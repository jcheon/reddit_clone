var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  }
})

var app2 = new Vue({
  el: '#app-2',
  data: {
    message: 'You loaded this page on ' + new Date().toLocaleString()
  }
})


var app3 = new Vue({
  el: '#app-3',
  data: {
    seen: true
  }
})


var app4 = new Vue({
  el: '#app-4',
  data: {
    suggestions: [],
    seen:true,
    unseen:false
  },
  //Adapted from https://stackoverflow.com/questions/36572540/vue-js-auto-reload-refresh-data-with-timer
  created: function() {
        this.fetchSuggestionList();
        this.timer = setInterval(this.fetchSuggestionList, 1000);
  },
  methods: {
    fetchSuggestionList: function() {
        axios
          .get('/suggestions/')
          .then(response => (this.suggestions = response.data.suggestions))
        console.log(this.suggestions)
        this.seen=false
        this.unseen=true
    },
    cancelAutoUpdate: function() { clearInterval(this.timer) }
  },
  beforeDestroy() {
    cancelAutoUpdate();
    clearInterval(this.timer)
  }

})

var app5 = new Vue({
  el: '#app-5',
  data: {
    subreddits: [],
    seen:true,
    unseen:false
  },

  created: function() {
    this.fetchSubredditList();
    this.timer = setInterval(this.fetchSubredditList, 1000);
  },
  methods: {
    fetchSubredditList: function() {
      axios
        .get('/getSubreddit/')
        .then(response => (this.subreddits = response.data.subreddits))
          console.log(this.subreddits)
        this.seen=false
        this.unseen=true
      },
    cancelAutoUpdate: function() { clearInterval(this.timer) }
  },
  beforeDestroy() {
    cancelAutoUpdate();
    clearInterval(this.timer)
  }
})