from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os, frontmatter as fm, re

home = "coffeeshop"
backend = "coffeeshopbackend"

file_loader = FileSystemLoader(f'{backend}\\templates')
env = Environment(loader=file_loader, autoescape=True)

pages = []

class page():
    def __init__(self, mdFile, address):
        self.home = "/" + home
        self.address = address
        self.path = self.address.split("/index.html")[0] # Removes the index.html from navbar links

        self.template = mdFile.get("template", "base_template")
        self.title = mdFile["title"]

        self.index = mdFile.get("index", 99)
        
        self.content = u"" + str(mdFile)

        if self.template == "menu":
            self.menu_items = mdFile.get("menu-items", {})
            print(self.menu_items)

    def data(self):        
        self.pages = pages # Get the top-level pages for the navbar.
        return vars(self) # Return a dictionary of values
    
    def make(self):
        if not os.path.exists(self.address):
            os.makedirs(self.address)
        
        try:
            template = env.get_template(self.template + "_template.html.j2")
        except TemplateNotFound:
            template = env.get_template("base_template.html.j2")
        with open(self.address, "wb") as file: # Use wb to allow encoding
            output = template.render(self.data())
            file.write(output.encode("utf-8")) # Need to encode otherwise characters like £ don't work

    def __repr__(self) -> str:
        return self.title


def mdToPage(path):
    mdFile = fm.load(path)

    address = ""

    # If it's a subpage, give it a folder, otherwise set it as the home page.
    if re.match(r".+index\.md", path):
        address = home + "/index.html"
    else:
        subdir = re.findall(f".+\/(.+)\.md", path)[0]
        address = f"{home}/{subdir}/index.html"

    pages.append(page(mdFile, address))

for filename in os.listdir(backend + "//pages"):
    mdToPage(backend + "//pages//" + filename)

# Sort navpages by index variable set in md files.
pages = [x for x in pages if x.address[-10:] == "index.html" ]
pages.sort(key=lambda x: x.index)

for page in pages:
    page.make()