# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Ansible Project

import pytest
from packaging.version import Version

import antsibull_core.ansible_core as ac


@pytest.mark. parametrize('version', ('2.9', '2.9.10', '1.0', '1', '0.7', '2.10', '2.10.0',
                                      '2.10.8', '2.10.12'))
def test_get_core_package_name_returns_ansible_base(version):
    assert ac.get_ansible_core_package_name(version) == 'ansible-base'
    assert ac.get_ansible_core_package_name(Version(version)) == 'ansible-base'


@pytest.mark.parametrize('version', ('2.11', '2.11.0', '2.11.8', '2.11.12', '2.13',
                                     '2.11.0a1', '3', '3.7.10'))
def test_get_core_package_name_returns_ansible_core(version):
    assert ac.get_ansible_core_package_name(version) == 'ansible-core'
    assert ac.get_ansible_core_package_name(Version(version)) == 'ansible-core'


@pytest.mark.parametrize('version, is_devel', [
    ('2.14.0dev0', True),
    ('2.14.0', False),
])
def test_get_core_package_name_returns_ansible_core(version, is_devel):
    assert ac._version_is_devel(Version(version)) == is_devel
