
def create_invoice():
    invoice_dict = {
        "type": "invoice",
        "message": "Your credits are too low to reply. Pay this invoice to add 100 credits and continue the conversation.",
        "link": "<Invoice Link>",
        "credits": 100
    }
    return invoice_dict




def check_credits(sender):
    return 100


def decrease_credits(sender):
    pass

