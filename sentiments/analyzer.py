import nltk

class Analyzer():
    """Implements sentiment analysis."""
    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positive_words = set()
        self.negative_words = set()

        # lees positive-words.txt
        file = open(negatives,'r')
        for i in file:
            self.negative_words.add(i.rstrip('\n'))
        file.close()

         # lees positive-words.txt
        file = open(positives,'r')
        for i in file:
            self.positive_words.add(i.rstrip('\n'))
        file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        # maakt van de text een token waardoor de tekst in losse worden gezien wordt.
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        score = 0
        for word in tokens:
            if word.lower() in self.positive_words:
                score += 1
            elif word.lower() in self.negative_words:
                score -= 1
            else:
                continue
        return score
