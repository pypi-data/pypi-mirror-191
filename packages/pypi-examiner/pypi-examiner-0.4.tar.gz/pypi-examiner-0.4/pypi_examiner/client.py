import requests
from bs4 import BeautifulSoup


class examiner(object):
    def __init__(self):
        pass

    def _extract_links(self, html, target, attributes):
        soup = BeautifulSoup(html, "html.parser")
        target_sections = soup.findAll(target, attrs=attributes)

        all_links = set()
        for target_section in target_sections:
            new_links = target_section.findAll("a")
            for new_link in new_links:
                if not new_link in all_links:
                    all_links.add(new_link)

        return list(all_links)

    def _fetch_package_page(self, package_name):
        url = f"https://pypi.org/project/{package_name}/"
        return requests.get(url)

    def _fetch_user_page(self, user_name):
        url = f"https://pypi.org/user/{user_name}/"
        return requests.get(url)

    def _strip_and_validate(self, href, split_len, prefix, select, suffix):
        href_components = href.split("/")

        if not len(href_components) == split_len:
            return False
        
        if not href.startswith(prefix):
            return False

        if not href.endswith(suffix):
            return False
        
        return href_components[select]

    def maintained_by(self, user_name):
        result = self._fetch_user_page(user_name)

        target_attrs = {"class": "package-list"}
        relevant_links = self._extract_links(result.text, "div", target_attrs)

        packages = set()
        for packages_link in relevant_links:
            href = packages_link["href"]
            package = self._strip_and_validate(href, 4, "/project/", 2, "/")
            if package:
                packages.add(package)

        return list(packages)

    def who_maintains(self, package_name):
        result = self._fetch_package_page(package_name)

        target_attrs = {"class": "sidebar-section__maintainer"}
        relevant_links = self._extract_links(result.text, "span", target_attrs)

        maintainers = set()
        for user_link in relevant_links:
            href = user_link["href"]
            user = self._strip_and_validate(href, 4, "/user/", 2, "/")
            if user:
                maintainers.add(user)

        return list(maintainers)

