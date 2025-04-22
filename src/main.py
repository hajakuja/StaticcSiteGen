from textnode import *
def main():
    textnode = TextNode("texty text is texting textily", TextType.LINK, "https://google.com")
    print(textnode)

if __name__ == "__main__":
    main()