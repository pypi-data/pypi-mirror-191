import typer
from pocket import Pocket, PocketException
import webbrowser

app = typer.Typer()


class PocketApp:
    DEFAULT_WORDS_PER_MINUTE = 180
    REDIRECT_URL = "https://cabeda.dev"

    def __init__(self):
        self.consumer_key = None
        self.access_token = None

        self._pocket = Pocket(None, None)

    def configure(self, consumer_key, access_token, words_per_minute, sort_field):
        self._pocket = Pocket(consumer_key, access_token)

    def init_consumer_key(self, consumer_key):
        self._pocket = Pocket(consumer_key, None)

    def get_request_token(self):
        return self._pocket.get_request_token(self.REDIRECT_URL)

    def get_access_token(self, request_token):
        return self._pocket.get_access_token(request_token)

    def fetch_newsletter(self):
        # Fetch a list of articles
        try:
            articles = self._pocket.retrieve(offset=0, tag="newsletter")

            if articles["list"] is not None:
                for key in articles["list"].keys():
                    title = articles["list"][key]["resolved_title"]
                    url = articles["list"][key]["resolved_url"]
                    markdown_link = f"- [{title}]({url})"
                    print(markdown_link)
            else:
                print("No articles with tag newsletter")

        except PocketException as e:
            print(e.message)


def configure(pocket_app: PocketApp, consumer_key, sort_field=10, words_per_minute=10):
    pocket_app.init_consumer_key(consumer_key)

    request_token = pocket_app.get_request_token()

    if not request_token:
        print("Could not obtain request_token")
        return

    url = (
        "http://getpocket.com/auth/authorize?request_token={0}"
        "&redirect_uri={1}".format(request_token, pocket_app.REDIRECT_URL)
    )

    print("You will have to authorize the application to access your articles")
    print("Enter any key once you're redirected to google.com")
    print("Or open this link in browser manually:")
    print(url)
    webbrowser.open_new_tab(url)
    input()

    access_token = pocket_app.get_access_token(request_token)

    if not access_token:
        print("Could not obtain access token")
        return

    pocket_app.configure(consumer_key, access_token, words_per_minute, sort_field)


@app.command()
def get(consumer_key: str = typer.Argument(None, envvar="POCKET_KEY")):
    pocket_app = PocketApp()

    if consumer_key is None:
        consumer_key = typer.prompt("What is the consumer_key?")

    configure(pocket_app, consumer_key)

    pocket_app.fetch_newsletter()


if __name__ == "__main__":
    app()
