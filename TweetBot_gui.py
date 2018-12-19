import tkinter
import tweepy

CONSUMER_KEY = 'Consumer Key'
CONSUMER_SECRET = 'Consumer Secret'
ACCESS_TOKEN = 'Access Token'
ACCESS_TOKEN_SECRET = 'Access Token Secret'

class TweetBotApplication:
    # builds TweetBot GUI 
    def __init__(self):
        self._root = tkinter.Tk()

        self._search_label = tkinter.Label(self._root, text="Search")
        self._search_entry = tkinter.Entry(self._root, bd=5)

        self._numTweetsLabel = tkinter.Label(self._root, text="Number of Tweets")
        self._numTweetsEntry = tkinter.Entry(self._root, bd=5)

        self._response_label = tkinter.Label(self._root, text="Response")
        self._response_entry = tkinter.Entry(self._root, bd=5)

        self._reply_label = tkinter.Label(self._root, text="Reply?")
        self._reply_entry = tkinter.Entry(self._root, bd=5)

        self._retweet_label = tkinter.Label(self._root, text="Retweet?")
        self._retweet_entry = tkinter.Entry(self._root, bd=5)

        self._favorite_label = tkinter.Label(self._root, text="Favorite?")
        self._favorite_entry = tkinter.Entry(self._root, bd=5)

        self._follow_label = tkinter.Label(self._root, text="Follow?")
        self._follow_entry = tkinter.Entry(self._root, bd=5)

        self._search_label.pack()
        self._search_entry.pack()

        self._numTweetsLabel.pack()
        self._numTweetsEntry.pack()

        self._response_label.pack()
        self._response_entry.pack()

        self._reply_label.pack()
        self._reply_entry.pack()

        self._retweet_label.pack()
        self._retweet_entry.pack()

        self._favorite_label.pack()
        self._favorite_entry.pack()

        self._follow_label.pack()
        self._follow_entry.pack()

        self.submit = tkinter.Button(self._root, text='Submit', command=self.start_bot)
        self.submit.pack(side=tkinter.BOTTOM)

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self._api = tweepy.API(auth)

        self.user = self._api.me()

    # runs TweetBot application
    def run(self):
        self._root.mainloop()
        
    def close_bot(self):
        self._root.destroy()

    # sets info_given to True if user clicks submit button and obtains all info for
    # actions user desires bot to perform
    def start_bot(self):
        self.search_info = self._search_entry.get()
        self.numberOfTweets = int(self._numTweetsEntry.get())
        self.phrase = self._response_entry.get()
        self.replyYN = self._reply_entry.get()
        self.retweetYN = self._retweet_entry.get()
        self.favoriteYN = self._favorite_entry.get()
        self.followYN = self._follow_entry.get()
        self.perform_action()

    # follows everyone back that is following the user
    def follow_back(self):
        for follower in tweepy.Cursor(self._api.followers).items():
            follower.follow()
            print ("Followed everyone that is following " + self.user.name)

    # retweets tweets based on specified keyword
    def retweet_keyword(self, search, numberOfTweets):
        for tweet in tweepy.Cursor(self._api.search, search).items(numberOfTweets):
            try:
                tweet.retweet()
                print('Retweeted the tweet')

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    # favorites tweets based on specified keyword
    def favorite_keyword(self, search, numberOfTweets):
        for tweet in tweepy.Cursor(self._api.search, search).items(numberOfTweets):
            try:
                tweet.favorite()
                print('Favorited the tweet')

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    # replys to a user based on keyword
    def reply_keyword(self, search, phrase, numberOfTweets):
        for tweet in tweepy.Cursor(self._api.search, search).items(numberOfTweets):
            try:
                print('\nTweet by: @' + tweet.user.screen_name)
                print('ID: @' + str(tweet.id))
                tweetId = tweet.id
                username = tweet.user.screen_name
                self._api.update_status("@" + username + " " + phrase, in_reply_to_status_id = tweetId)
                print("Replied with " + phrase)

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break

    def perform_action(self):
        if self.replyYN.lower() == 'yes':
            self.reply_keyword(self.search_info, self.phrase, self.numberOfTweets)
        if self.retweetYN.lower() ==  'yes':
            self.retweet_keyword(self.search_info, self.numberOfTweets)
        if self.favoriteYN.lower() == 'yes':
            self.favorite_keyword(self.search_info, self.numberOfTweets)
        if self.followYN.lower() == 'yes':
            self.follow_back()



if __name__ == '__main__':
    TweetBotApplication().run()
