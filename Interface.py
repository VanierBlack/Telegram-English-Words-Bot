from libraries import *
import argparse

def SendWords():
    import EnglishBot
    EnglishBot.main()

def CreatePoll(question, options, correct_answer):
	import EnglishBot
	EnglishBot.CreatePoll(question, options, correct_answer)

def DeleteMessage(id):
	import EnglishBot
	EnglishBot.DeleteMessage(id)

def TrackMessages():
	import EnglishBot
	EnglishBot.InitiateMessagesTracking()
	
parser = argparse.ArgumentParser(prog="EnglishBot", 
    description="Send English Vocabularies Daily")

parser.add_argument("-s", "--SendMessages", action="store_true", help="Send messages")
parser.add_argument("-p", "--Quiz", action = "store_true", help = "Creating Quizes")
parser.add_argument("-q", "--Question", action = "append", help = "Providing Question for the Quiz")
parser.add_argument("-o", "--Options", action = "append", help = "Providing Options for the Quiz", nargs = "*")
parser.add_argument("-a", "--Answer", action = "append", help = "Providing the correct answer", nargs = 1)
parser.add_argument("-d", "--DeleteMessage", action = "append", help = "Delete a specific message", nargs = 1)
parser.add_argument("-t", "--TrackMessages", action = "store_true", help = "Track Messages Sent")
args = parser.parse_args()

if args.SendMessages:
	SendWords()

if args.Quiz:
	if args.Question and (2 <= len(*args.Options) <= 5):
		CreatePoll(args.Question, *args.Options, *args.Answer)
		print("Poll Sent Successfully")

if args.DeleteMessage:
	message_id = int(*args.DeleteMessage[0])
	DeleteMessage(message_id)

if args.TrackMessages:
	TrackMessages()

