import importlib.machinery
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS=Path(__file__).resolve().parents[1]/'tools'
sys.path.insert(0,str(TOOLS))
from rl_network import on_lab_network


def module(name):
    loader=importlib.machinery.SourceFileLoader(name.replace('-','_'),str(TOOLS/name))
    spec=importlib.util.spec_from_loader(loader.name,loader)
    obj=importlib.util.module_from_spec(spec);loader.exec_module(obj)
    return obj


class NetworkTests(unittest.TestCase):
    def test_membership_uses_full_cidr(self):
        for address,expected in [('192.0.2.65/24',True),('192.0.2.126',True),
                                 ('192.0.2.63',False),('192.0.2.128/24',False)]:
            with self.subTest(address=address):
                self.assertEqual(on_lab_network(address,'192.0.2.64/26'),expected)

    def test_invalid_and_missing_scope_fail_closed(self):
        for network in ('','not-a-network','192.0.2.65/26','::/0'):
            with self.subTest(network=network):
                self.assertFalse(on_lab_network('192.0.2.65',network))
        with patch.dict(os.environ,{},clear=True):
            self.assertFalse(on_lab_network('192.0.2.65'))

    def test_listener_does_not_discover_ap_outside_scope(self):
        tool=module('robot-listen')
        with patch.dict(os.environ,{'RL_LAB_NETWORK':'192.0.2.64/26'}), \
             patch.object(tool,'my_ip',return_value='198.51.100.9/24'), \
             patch.object(tool,'find_ap',side_effect=AssertionError('AP discovery must be gated')):
            with tempfile.TemporaryDirectory() as folder, patch.object(tool,'OUTDIR',Path(folder)):
                result=tool.preflight(verbose=False)
        self.assertFalse(result[0])

    def test_wired_preflight_does_not_contact_host_outside_scope(self):
        tool=module('wire-listen')
        local=subprocess.CompletedProcess([],0,'eth0 UP 198.51.100.9/24\n','')
        with patch.dict(os.environ,{'RL_LAB_NETWORK':'192.0.2.64/26'}), \
             patch.object(tool.subprocess,'run',return_value=local), \
             patch.object(tool,'ssh',side_effect=AssertionError('SSH must be gated')):
            self.assertFalse(tool.preflight('example.invalid',None,verbose=False)[0])

    def test_unattended_scope_failure_stops_before_remote_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp)
            for name in ('ssh','ssh-keyscan'):
                p=folder/name;p.write_text('#!/bin/sh\necho contacted >> "$TEST_CONTACTS"\nexit 1\n');p.chmod(0o755)
            p=folder/'ip';p.write_text('#!/bin/sh\necho "eth0 UP 198.51.100.9/24"\n');p.chmod(0o755)
            mark=folder/'contacts'
            env={**os.environ,'PATH':str(folder)+os.pathsep+os.environ['PATH'],
                 'RL_LAB_NETWORK':'192.0.2.64/26','TEST_CONTACTS':str(mark)}
            done=subprocess.run(['bash',str(TOOLS/'rl-unattended-capture'),'--check'],
                                env=env,capture_output=True,text=True,timeout=10)
            self.assertEqual(done.returncode,2,done.stdout+done.stderr)
            self.assertFalse(mark.exists())

    def test_shell_scripts_parse_without_execution(self):
        for p in TOOLS.iterdir():
            if p.is_file() and p.read_text().startswith('#!/usr/bin/env bash'):
                with self.subTest(script=p.name):
                    done=subprocess.run(['bash','-n',str(p)],capture_output=True,text=True)
                    self.assertEqual(done.returncode,0,done.stderr)

    def test_rehearsal_does_not_contact_management_hosts(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);mark=folder/'contacts'
            for name in ('ssh','ssh-keyscan'):
                p=folder/name;p.write_text('#!/bin/sh\necho contacted >> "$TEST_CONTACTS"\nexit 1\n');p.chmod(0o755)
            p=folder/'ip';p.write_text('#!/bin/sh\necho "eth0 UP 192.0.2.65/26"\n');p.chmod(0o755)
            env={**os.environ,'PATH':str(folder)+os.pathsep+os.environ['PATH'],
                 'RL_LAB_NETWORK':'192.0.2.64/26','OUTDIR':str(folder/'output'),
                 'TEST_CONTACTS':str(mark),'TERM':'dumb'}
            for name in ('robot-roll-call','robot-round-up'):
                with self.subTest(tool=name):
                    done=subprocess.run(['bash',str(TOOLS/name),'--dry-run'],input='\n',
                                        env=env,capture_output=True,text=True,timeout=10)
                    self.assertEqual(done.returncode,2,done.stdout+done.stderr)
                    self.assertRegex(done.stdout,r'Input ended at a pause|No input\. Nothing was started')
                    self.assertFalse(mark.exists())

    def test_moved_host_records_only_already_trusted_key_algorithms(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);sshdir=folder/'.ssh';sshdir.mkdir()
            known=sshdir/'known_hosts';known.write_text('oldhost ssh-ed25519 trustedKey\n')
            keyscan=folder/'ssh-keyscan'
            keyscan.write_text('#!/bin/sh\nprintf "newhost ssh-ed25519 trustedKey\\nnewhost ssh-rsa unexpectedKey\\n"\n')
            keyscan.chmod(0o755)
            keygen=folder/'ssh-keygen'
            keygen.write_text('''#!/bin/sh
if [ "$1" = "-F" ]; then exit 1; fi
if [ "$2" != "-" ]; then echo '256 SHA256:known oldhost'; exit 0; fi
while IFS= read -r line; do
  case "$line" in
    *trustedKey*) echo '256 SHA256:known host' ;;
    *unexpectedKey*) echo '256 SHA256:untrusted host' ;;
  esac
done
''')
            keygen.chmod(0o755)
            env={**os.environ,'HOME':str(folder),'PATH':str(folder)+os.pathsep+os.environ['PATH']}
            done=subprocess.run(['bash',str(TOOLS/'ap-hostkey'),'newhost'],env=env,
                                capture_output=True,text=True,timeout=10)
            self.assertEqual(done.returncode,3,done.stdout+done.stderr)
            self.assertIn('newhost ssh-ed25519 trustedKey',known.read_text())
            self.assertNotIn('unexpectedKey',known.read_text())


if __name__=='__main__':unittest.main()
