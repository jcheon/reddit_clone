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
    fetchSuggestionList: function(arg) {
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
        .get('/getSubreddit')
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

var app6 = new Vue({
  el: '#app-6',
  data: {
    chatrooms: [],
    seen:true,
    unseen:false
  },

  created: function() {
    this.fetchChatroomList();
    this.timer = setInterval(this.fetchChatroomList, 1000);
  },
  methods: {
    fetchChatroomList: function() {
      axios
        .get('/getChatrooms/')
        .then(response => (this.chatrooms = response.data.chatrooms))
          console.log(this.chatrooms)
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

var app7 = new Vue({
  el: '#app-7',
  data: {
    suggestions: []
  },

  created: function() {
    this.fetchSubPostList();
    this.timer = setInterval(this.fetchSubPostList, 1000);
  },
  methods: {
    fetchSubPostList: function() {
      // console.log(document.getElementById("curSub").innerHTML.split("/")[1].split("<")[0]);
      // subreddit = document.getElementById("curSub").innerHTML.split("/")[1].split("<")[0];
      axios
        .get('/getSubPosts/' + document.getElementById("curSub").innerHTML.split("/")[1].split("<")[0] + '/')
        .then(response => (this.suggestions = response.data.suggestions))
          console.log(this.suggestions)
      },
    cancelAutoUpdate: function() { clearInterval(this.timer) }
  },
  beforeDestroy() {
    cancelAutoUpdate();
    clearInterval(this.timer)
  }
})

var app8 = new Vue({
  el: '#app-8',
  data: {
    suggestions: []
  },

  created: function() {
    this.fetchPost();
    this.timer = setInterval(this.fetchPost, 1000);
  },
  methods: {
    fetchPost: function() {
      axios
        .get('/getPost/' + document.getElementById("curPost").innerHTML.split("/")[1].split("<")[0] + '/')
        .then(response => (this.suggestions = response.data.suggestions))
          console.log(this.suggestions)
      },
    cancelAutoUpdate: function() { clearInterval(this.timer) }
  },
  beforeDestroy() {
    cancelAutoUpdate();
    clearInterval(this.timer)
  }
})






