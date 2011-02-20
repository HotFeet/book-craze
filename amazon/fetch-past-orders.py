import sys
import datetime
import mechanize
from optparse import OptionParser  
from BeautifulSoup import BeautifulSoup
from lxml import etree

"""
Usage: python fetch-past-orders.py --username=foo --password=bar --firstyear=2004
"""

def getOptions():
   arguments = OptionParser()
   arguments.add_options(["--username", "--password", "--firstyear"])
   return arguments.parse_args()[0]

def _text(node):
      return "".join([unicode(s) for s in node.contents]).strip()

def _list_item_value(ul, item_key):
		b = ul.find("b", text=item_key)
		try:
			return b.parent.nextSibling.strip()
		except AttributeError:
			return ""

def _parse_book_infos(html, book):
		soup = BeautifulSoup(html)

		info_div = soup.find("h2", text="Produktinformation").parent.nextSibling.nextSibling
		info = info_div.findAll("ul")[0]
		book.set("isbn", _list_item_value(info, "ISBN-10:"))
		del book.attrib["link"]

def _parse_orders(html):
      soup = BeautifulSoup(html)
      books = []
      for order in soup.findAll("div", {"class": "order"}):
            date = order.find("h2")
            for item in order.findAll("li", {"class": "item "}):
                  title = item.find("span", {"class": "item-title"})
                  link = item.find("a")
                  books.append(etree.Element("book",
                        order_date = _text(date),
                        title = _text(title),
                        link = link["href"]
                  ))

      return books

if __name__ == '__main__': 

      options = getOptions()

      br = mechanize.Browser()
      br.set_handle_robots(False)
      br.addheaders = [("User-agent", "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Fedora/3.6.13-1.fc13 Firefox/3.6.13")]

      sign_in = br.open("http://www.amazon.de/gp/flex/sign-out.html")

      br.select_form(name="sign-in")
      br["email"] = options.username
      br["password"] = options.password
      logged_in = br.submit()

      error_str = "The e-mail address and password you entered do not match any accounts on record."
      if error_str in logged_in.read():
            print error_str
            sys.exit(1)

      books = etree.Element("books")
      for year in range(int(options.firstyear),  datetime.datetime.now().year):
            orders_html = br.open("https://www.amazon.de/gp/css/history/orders/view.html?orderFilter=year-%s&startAtIndex=1000" % year)
            new_books = _parse_orders(orders_html.read())
            if new_books:
                  for book in new_books:
                        book_info_html = br.open(book.get("link"))
                        _parse_book_infos(book_info_html.read(), book)
                        books.append(book)

      print(etree.tostring(books, pretty_print=True))

