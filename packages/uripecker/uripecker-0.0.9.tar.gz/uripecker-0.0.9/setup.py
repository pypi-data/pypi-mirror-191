from distutils.core import setup

import re
import sys

VDK_KNOWN_LICENSES = [
    'License :: Aladdin Free Public License (AFPL)',
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'License :: CeCILL-B Free Software License Agreement (CECILL-B)',
    'License :: CeCILL-C Free Software License Agreement (CECILL-C)',
    'License :: DFSG approved',
    'License :: Eiffel Forum License (EFL)',
    'License :: Free For Educational Use',
    'License :: Free For Home Use',
    'License :: Free To Use But Restricted',
    'License :: Free for non-commercial use',
    'License :: Freely Distributable',
    'License :: Freeware',
    'License :: GUST Font License 1.0',
    'License :: GUST Font License 2006-09-30',
    'License :: Netscape Public License (NPL)',
    'License :: Nokia Open Source License (NOKOS)',
    'License :: OSI Approved',
    'License :: OSI Approved :: Academic Free License (AFL)',
    'License :: OSI Approved :: Apache Software License',
    'License :: OSI Approved :: Apple Public Source License',
    'License :: OSI Approved :: Artistic License',
    'License :: OSI Approved :: Attribution Assurance License',
    'License :: OSI Approved :: BSD License',
    'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)',
    'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',
    'License :: OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)',
    'License :: OSI Approved :: Common Public License',
    'License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)',
    'License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)',
    'License :: OSI Approved :: Eiffel Forum License',
    'License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)',
    'License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)',
    'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'License :: OSI Approved :: GNU Free Documentation License (FDL)',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
    'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'License :: OSI Approved :: Historical Permission Notice and Disclaimer (HPND)',
    'License :: OSI Approved :: IBM Public License',
    'License :: OSI Approved :: ISC License (ISCL)',
    'License :: OSI Approved :: Intel Open Source License',
    'License :: OSI Approved :: Jabber Open Source License',
    'License :: OSI Approved :: MIT License',
    'License :: OSI Approved :: MIT No Attribution License (MIT-0)',
    'License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)',
    'License :: OSI Approved :: MirOS License (MirOS)',
    'License :: OSI Approved :: Motosoto License',
    'License :: OSI Approved :: Mozilla Public License 1.0 (MPL)',
    'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)',
    'License :: OSI Approved :: Nethack General Public License',
    'License :: OSI Approved :: Nokia Open Source License',
    'License :: OSI Approved :: Open Group Test Suite License',
    'License :: OSI Approved :: Open Software License 3.0 (OSL-3.0)',
    'License :: OSI Approved :: PostgreSQL License',
    'License :: OSI Approved :: Python License (CNRI Python License)',
    'License :: OSI Approved :: Python Software Foundation License',
    'License :: OSI Approved :: Qt Public License (QPL)',
    'License :: OSI Approved :: Ricoh Source Code Public License',
    'License :: OSI Approved :: SIL Open Font License 1.1 (OFL-1.1)',
    'License :: OSI Approved :: Sleepycat License',
    'License :: OSI Approved :: Sun Industry Standards Source License (SISSL)',
    'License :: OSI Approved :: Sun Public License',
    'License :: OSI Approved :: The Unlicense (Unlicense)',
    'License :: OSI Approved :: Universal Permissive License (UPL)',
    'License :: OSI Approved :: University of Illinois/NCSA Open Source License',
    'License :: OSI Approved :: Vovida Software License 1.0',
    'License :: OSI Approved :: W3C License',
    'License :: OSI Approved :: X.Net License',
    'License :: OSI Approved :: Zope Public License',
    'License :: OSI Approved :: zlib/libpng License',
    'License :: Other/Proprietary License',
    'License :: Public Domain',
    'License :: Repoze Public License',
]


def vdk_cleanup(value):
    """
    Remove unexpanded vdk-pylib macros from value
    """

    def has_macro(S):
        return (
            bool(re.match('.*__VDK_PYLIB_[A-Z][A-Z0-9_]*__.*', S.strip()))
            or bool(re.match('.*__MKIT_[A-Z][A-Z0-9_]*__.*', S.strip()))
        )

    def vdk_cleanup_str(value):
        if has_macro(value):
            return ''
        return value.strip()

    def vdk_cleanup_list(value):
        if len(value) == 1:
            if has_macro(value[0]):
                return []
        return value

    if type(value) is str:
        return vdk_cleanup_str(value)
    if type(value) is list:
        return vdk_cleanup_list(value)
    else:
        raise NotImplementedError(f"cannot cleanup: {type(value)}")


VDK_PYLIB_DESCRIPTION = """
uripecker takes text and finds URLs.  Along
with URLs it also supports several forms
of short-hand indentifiers such as "bug 1234",
which it can also locate and translate to URLs
according to provided mapping.
"""

VDK_PYLIB_PKGMAP = [
    '__VDK_PYLIB_PKGMAP__',
]

VDK_PYLIB_DEFAULT_PKGMAP = """
uripecker src/uripecker py.typed
"""

VDK_PYLIB_REQUIRES_PYSTUFF = [
    'neaty',
]

VDK_PYLIB_CLASSIFIERS_OVERRIDE = [
    '__VDK_PYLIB_CLASSIFIERS_OVERRIDE__',
]

VDK_PYLIB_CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Natural Language :: English',
]

VDK_PYLIB_PYTHON_GE = """
3.9
"""

VDK_PYLIB_PYTHON_LT = """
3.11
"""

MKIT_PROJ_LICENSE = """
LGPLv2
"""


class PackageMapItem:

    @classmethod
    def from_line(cls, line):
        words = line.split()
        name = words.pop(0)
        directory = words.pop(0)
        files = words
        return cls(name, directory, files)

    def __init__(self, name, directory, files):
        self.name = name
        self.directory = directory
        self.files = files


class PackageMap:

    @classmethod
    def from_macros(cls):
        def from_pkgmap():
            items = []
            for line in vdk_cleanup(VDK_PYLIB_PKGMAP):
                try:
                    items.append(PackageMapItem.from_line(line))
                except Exception:
                    print(f"skipping invalid item: {line!r}", file=sys.stderr)
            return items
        default_items = [
            PackageMapItem.from_line(vdk_cleanup(VDK_PYLIB_DEFAULT_PKGMAP))
        ]
        return cls(
            items=from_pkgmap() or default_items,
        )

    def __init__(self, items):
        self.items = items

    @property
    def names(self):
        return [i.name for i in self.items]

    @property
    def dirs(self):
        out = {}
        for item in self.items:
            out[item.name] = item.directory
        return out

    @property
    def files(self):
        out = {}
        for item in self.items:
            out[item.name] = item.files
        return out

    def as_dict(self):
        return {
            'packages': self.names,
            'package_dir': self.dirs,
            'package_data': self.files,
        }


class License:

    @classmethod
    def from_macros(cls):
        def find_classifier(S):
            suffix = f'({S})'
            for classifier in VDK_KNOWN_LICENSES:
                if classifier.endswith(suffix):
                    return classifier
            raise ValueError(
                f"could not find license classifier for: {S!r}"
            )
        shortname = vdk_cleanup(MKIT_PROJ_LICENSE)
        classifier = find_classifier(shortname)
        return cls(
            shortname=shortname,
            classifier=classifier,
        )

    def __init__(self, shortname, classifier):
        self.shortname = shortname
        self.classifier = classifier


class VersionNumber:

    @classmethod
    def from_text(cls, text):
        try:
            tx, ty = text.split('.', maxsplit=1)
            x, y = int(tx), int(ty)
        except Exception:
            raise ValueError(f"could not parse Python 3 version: {text}")
        if x != 3:
            raise ValueError(f"only Python 3 versions are supported: {text}")
        return cls(x, y)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}.{self.y}"

    def __lt__(self, othr):
        return (self.x, self.y) < (othr.x, othr.y)

    def range_to(self, othr):
        if othr < self:
            raise ValueError(f"impossible version range: {self} to {othr}")
        for rx in range(self.x, othr.x+1):
            for ry in range(self.y, othr.y):
                yield self.__class__(rx, ry)

    def as_classifier(self):
        return f'Programming Language :: Python :: {self.x}.{self.y}'


class VersionRange:

    implied_classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ]

    @classmethod
    def from_macros(cls):
        ver_ge_txt = vdk_cleanup(VDK_PYLIB_PYTHON_GE) or '3.0'
        ver_lt_txt = vdk_cleanup(VDK_PYLIB_PYTHON_LT) or '3.12'
        ver_ge = VersionNumber.from_text(ver_ge_txt)
        ver_lt = VersionNumber.from_text(ver_lt_txt)
        return cls(
            versions=ver_ge.range_to(ver_lt)
        )

    def __init__(self, versions):
        self.versions = versions

    @property
    def classifiers(self):
        by_range = [v.as_classifier() for v in self.versions]
        return sorted(set(by_range + self.implied_classifiers))


class PackageMeta:

    @classmethod
    def from_macros(cls):
        def vdk_classifiers():
            ovr = vdk_cleanup(VDK_PYLIB_CLASSIFIERS_OVERRIDE) or []
            main = vdk_cleanup(VDK_PYLIB_CLASSIFIERS) or []
            return ovr or main
        vrange = VersionRange.from_macros()
        classifiers = sorted(set(vdk_classifiers() + vrange.classifiers))
        return cls(
            classifiers=classifiers,
        )

    def __init__(self, classifiers):
        self.classifiers = classifiers

    def as_dict(self):
        return {
            'classifiers': self.classifiers,
        }


def vdk_packageinfo():
    pmap = PackageMap.from_macros()
    pmeta = PackageMeta.from_macros()
    return pmap.as_dict() | pmeta.as_dict()


setup(
    description='uripecker - Peck them URIs out',
    license='LGPLv2',
    long_description=vdk_cleanup(VDK_PYLIB_DESCRIPTION),
    maintainer_email='Alois Mahdal <netvor+uripecker@vornet.cz>',
    name='uripecker',
    packages=vdk_packageinfo()['packages'],
    package_dir=vdk_packageinfo()['package_dir'],
    package_data=vdk_packageinfo()['package_data'],
    url='https://gitlab.com/vornet/python/python-uripecker',
    requires=vdk_cleanup(VDK_PYLIB_REQUIRES_PYSTUFF),
    version='0.0.9',
    classifiers=vdk_packageinfo()['classifiers'],
)

# setup.py built with MKit 0.0.60 and vdk-pylib-0.0.25
