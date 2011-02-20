using System;
using System.Text.RegularExpressions;
using System.Xml;
using System.Net;
using Newtonsoft.Json;

namespace HotFeet.FunStuff {
	public static class BookInfoLoader {
		static readonly string urlTemplate = "http://openlibrary.org/api/books?bibkeys=ISBN:{0}&format=json&jscmd=details";
		static readonly Regex wrappedData = new Regex(@"\{.*?(\{.+\}).*?\}");
		static readonly WebClient wc = new WebClient();
		
		public static string LoadJson(string isbn) {
			string url = String.Format(urlTemplate, isbn);
			return wc.DownloadString(url);
		}
		
		public static XmlDocument LoadXml(string isbn) {
			string json = LoadJson(isbn);

			// unwrap data by removing outermost json dictionary
			// e.g. "{'ISBN:0091929784': { ..... }}" => "{ ..... }"
			json = wrappedData.Replace(json, "$1");

			return JsonConvert.DeserializeXmlNode(json, "book_info");
		} 

		/*** Driver ***/
		static void Main(string[] args) {
			XmlDocument xml = LoadXml(args[0]);
			xml.Save(Console.Out);
			
			Console.WriteLine();
			string coverUrl = String.Format(
				"http://covers.openlibrary.org/b/isbn/{0}-L.jpg",
				args[0]
			);
			Console.WriteLine(coverUrl);
		}
	}
}

/*** Regex ***/
"{'ISBN:0091929784': { ..... }}" => "{ ..... }"

-> "{.*{.*} *}"

-> "{.*?{.*} *}"       (make start non-eager)

-> "{.*?({.*}) *}"     (group middle part)

-> "\{.*?(\{.*\}) *\}" (escape '{' and '}')
