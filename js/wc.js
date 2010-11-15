/*

A list of words, where the size and color of each word is determined
by the number of times it appears in the text.
Uses the Google Visalization API.

Data Format
  Any number of rows and columns.
  All string values are concatenated, other column types are ignored.

Configuration options:
  none

Methods
  none

Events
  none

*/

WordCloud = function(container) {
  this.container = container;
}

WordCloud.DEFAULT_STOP_WORDS = {
  "a": 1,
  "an": 1,
  "and": 1,
  "is": 1,
  "or": 1,
  "the": 1
};

// Add all word in a given text to a list and map.
// list is a list of unique words.
// map is a set of all found words.
// stopWords is a set of all words to ignore.
WordCloud.addWords = function(text, list, map, stopWords) {
  var word = '';
  for (var i = 0; i < text.length; i++) {
    var c = text.charAt(i);
    if (' ,.<>[]{}/`~!@#$%^&*()-_=+\'"\\|:;?\r\r\n'.indexOf(c) >= 0) {
      if (word.length > 1) {
        WordCloud.addWord(word, list, map, stopWords);
      }
      word = '';
    } else {
      word += c;
    }
  }
  if (word.length > 0) {
    WordCloud.addWord(word, list, map, stopWords);
  }
};

// Add a single word to a list and map.
// list is a list of unique words.
// map is a set of all found words.
// stopWords is a set of all words to ignore.
WordCloud.addWord = function(word, list, map, stopWords) {
  var wl = word.toLowerCase();
  if (stopWords[wl]) {
    return; // Ignore stop words
  }
  if (map[wl]) {
    map[wl]++;
  } else {
    map[wl] = 1;
    list.push(word);
  }
};

WordCloud.MIN_UNIT_SIZE = 1;
WordCloud.MAX_UNIT_SIZE = 7;
WordCloud.RANGE_UNIT_SIZE = WordCloud.MAX_UNIT_SIZE - WordCloud.MIN_UNIT_SIZE;

WordCloud.prototype.draw = function(data, options) {

  var wordMap = {};
  var wordList = [];

  options = options || {};
  var stopWords = WordCloud.DEFAULT_STOP_WORDS;
  if (options.stopWords) {
    stopWords = {};
    var words = options.stopWords.toLowerCase().split(/ |,/);
    for (var i = 0; i < words.length; i++) {
      stopWords[words[i]] = 1;
    }
  }

  for (var rowInd = 0; rowInd < data.getNumberOfRows(); rowInd++) {
    for (var colInd = 0; colInd < data.getNumberOfColumns(); colInd++) {
      if (data.getColumnType(colInd) == 'string') {
        WordCloud.addWords(data.getValue(rowInd, colInd), wordList, wordMap, stopWords);
      }
    }
  }

  // Compute frequency range
  var minFreq = 999999;
  var maxFreq = 0;
  for (var word in wordMap) {
    var f = wordMap[word];
    minFreq = Math.min(minFreq, f);
    maxFreq = Math.max(maxFreq, f);
  }
  var range = maxFreq - minFreq;
  range = Math.max(range, 4);

  // Idea: Add option to sort by text, freq or no sort

  var html = [];
  html.push('<div class="word-cloud">');
  for (var i = 0; i < wordList.length; i++) {
    var word = wordList[i];
    var text = word;
    var freq = wordMap[word.toLowerCase()];
    if (freq > 1)
	{
		var size = WordCloud.MIN_UNIT_SIZE +
	         Math.round((freq - minFreq) / range * WordCloud.RANGE_UNIT_SIZE);
	    html.push('<span class="word-cloud-', size, '">', text, '</span> ');
	  }
	}
	
  html.push('</div>');

  this.container.innerHTML = html.join('');
};

