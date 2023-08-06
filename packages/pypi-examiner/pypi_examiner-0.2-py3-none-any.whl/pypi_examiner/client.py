import requests
from bs4 import BeautifulSoup


class examiner(object):
    def __init__(self):
        pass

    def _fetch_package_page(self, package_name):
        url = f"https://pypi.org/project/{package_name}/"
        return requests.get(url)

    def who_owns(self, package_name):
        result = self._fetch_package_page(package_name)
        soup = BeautifulSoup(result.text, "html.parser")

        maintainers = set()

        maint_span = soup.findAll(
            "span", attrs={"class": "sidebar-section__maintainer"}
        )

        for maint_divs in maint_span:
            maint_links = maint_divs.findAll("a")
            for maint_link in maint_links:
                maint_components = maint_link["href"].split("/")  # ex. /user/tweedge/
                maintainers.add(maint_components[2])

        return list(maintainers)
