from summarizer import summarize


data= data["unshorted-text"]


def convert_text(title, text):
    return summarize(title, text, count = 2)

newsletter_short= {
    "title"           : "Titel",
    "shorted-text"  : convert_text(Name['unshorted_text'], Name['title']),
    "link"            : "https://*/*",
    "date"            : "",
    "id"              : "<replace(title, ' ', '-) + date>"
  }




