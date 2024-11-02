from libraries import *
import argparse
import EnglishBot


def SendWords():
    EnglishBot.main()

def CreatePoll(question, options, correct_answer):
    EnglishBot.CreatePoll(question, options, correct_answer)

def DeleteMessage(id):
    EnglishBot.DeleteMessage(id)

def TrackMessages():
    with EnglishBot.bot_lock:
        EnglishBot.InitiateMessagesTracking()
        EnglishBot.bot.polling(none_stop=True, interval=5)

parser = argparse.ArgumentParser(prog="EnglishBot", 
    description="Send English Vocabularies Daily")

parser.add_argument("-s", "--SendMessages", action="store_true", help="Send messages")
parser.add_argument("-p", "--Quiz", action="store_true", help="Creating Quizes")
parser.add_argument("-q", "--Question", action="append", help="Providing Question for the Quiz")
parser.add_argument("-o", "--Options", action="append", help="Providing Options for the Quiz", nargs="*")
parser.add_argument("-a", "--Answer", action="append", help="Providing the correct answer", nargs=1)
parser.add_argument("-d", "--DeleteMessage", action="append", help="Delete a specific message", nargs=1)
parser.add_argument("-t", "--TrackMessages", action="store_true", help="Track Messages Sent")
args = parser.parse_args()

if args.SendMessages:
    SendWords()

if args.Quiz:
    if args.Question and args.Options and args.Answer:
        question = args.Question[0]
        options = args.Options[0]
        correct_answer = args.Answer[0]
        
        if 2 <= len(options) <= 5:
            CreatePoll(question, options, correct_answer)
            print("Poll Sent Successfully")
        else:
            print("Invalid number of options. Must be between 2 and 5.")
    else:
        print("Missing required arguments for creating a quiz.")

    if args.TrackMessages:
        thread = threading.Thread(target=TrackMessages)
        thread.start()

if args.DeleteMessage:
    message_id = int(args.DeleteMessage[0][0])
    DeleteMessage(message_id)

if args.TrackMessages:
    TrackMessages()