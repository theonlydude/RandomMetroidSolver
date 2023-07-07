echo "begin tracker pull"
cd $(dirname $0)

NEW_RELEASE=$(curl -s https://api.github.com/repos/chriscauley/super-metroid/releases/latest | jq -r '.assets[0].browser_download_url')

rm -rf client
echo "${NEW_RELEASE}"
echo "${NEW_RELEASE}" | wget -qi - && tar zxf release.tar.gz && rm -f release.tar.gz
./install.sh

echo "end tracker pull"
