# Maintainer: Michael John <amstelchen at gmail dot com>

pkgname=goalfm
_pkgname=GoalFM
pkgver=1.0.7
pkgrel=1
pkgdesc='A managerial sports game written in Python.'
arch=('any')
url="http://github.com/amstelchen/GoalFM"
license=('CPL')
depends=('python3')
makedepends=('python-setuptools')
#source=("https://files.pythonhosted.org/packages/2e/a9/9c6ad02f88918c868b737c69eea9e775fbf96dd1c72444e1f1e7534740b8/${_pkgname}-${pkgver}.tar.gz")
#sha256sums=('e7bce450b58767bab48c55e7dbee8557ff142309581d24789d9510a1f3cade58')
md5sums=('22097f9982f5a724d3193206e3b6dffd')
source=("${_pkgname}-${pkgver}.tar.gz")

build() {
  cd "${srcdir}/${_pkgname}-${pkgver}"
  python setup.py build
}

package() {
  cd "${srcdir}/${_pkgname}-${pkgver}"
  python setup.py install --root="${pkgdir}/" --optimize=1 --skip-build

  install -Dm644 "${srcdir}/${_pkgname}-${pkgver}"/assets/GoalFM.png \
      "${pkgdir}"/usr/share/pixmaps/GoalFM.png
  install -Dm644 "${srcdir}/${_pkgname}-${pkgver}"/assets/GoalFM.desktop \
      "${pkgdir}"/usr/share/applications/GoalFM.desktop
}
