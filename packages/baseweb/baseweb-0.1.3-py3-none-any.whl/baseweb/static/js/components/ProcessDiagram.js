Vue.component("ProcessStep", {
  template: `
    <li v-if="'label' in step">
      <div class="step">
        <div class="header">
          <h4>{{ step.label }}</h4>
        </div>
        <div class="body">
          <table width="100%">
          <tr v-for="(value, key) in step.data" :key="key">
            <th>{{ key }}</th><td align="right">{{ value }}</td>
          </tr>
          </table>
        </div>
      </div>
    </li>
    <li v-else-if="'sequence' in step && child">
      <ol>
        <ProcessStep v-for="(childstep, i) in step.sequence" :step="childstep" :key="i" child="true"/>
      </ol>
    </li>
    <ol v-else-if="'sequence' in step && ! child" class="process_diagram">
      <ProcessStep v-for="(childstep, i) in step.sequence" :step="childstep" :key="i" child="true"/>
    </ol>
    <li v-else-if="'fanout' in step">
      <ul>
        <ProcessStep v-for="(childstep, i) in step.fanout" :step="childstep" :key="i" child="true"/>
      </ul>
    </li>
`,
  props: [ "step", "child" ]
});

Vue.component("ProcessDiagram", {
  template: `
  <v-card>
    <v-card-actions>
      <h2>{{ title }}</h2>
      <v-spacer></v-spacer>
      <v-btn icon @click="play()" v-if="!playing">
        <v-icon>play_arrow</v-icon>
      </v-btn>
      <v-btn icon @click="stop()" v-if="playing">
        <v-icon>stop</v-icon>
      </v-btn>
      <v-btn icon @click="reset()">
        <v-icon>replay</v-icon>
      </v-btn>
    </v-card-actions>
    <v-card-text>
      <ProcessStep :step="diagram"/>
    </v-card-text>
  </v-card>
`,
  props: [ "title", "id" ],
  created: function() {
    if( store.getters.env("FA_URL") ) {
      this.fetch_stats();
    } else {
      var self = this;
      store.subscribe( function(mutation, state) {
        if( mutation.type === "updated_env" && "FA_URL" in mutation.payload ) {
          self.fetch_stats();
        }
      });
    }
  },
  beforeDestroy: function() {
    this.playing = false;
    if(this.poller) { clearTimeout(this.poller); }
  },
  computed: {
    diagram: function() {
      var self = this;
      function fill_stats(s) {
        if( "sequence" in s) {
          var l = [];
          for(var child in s["sequence"]) {
            l.push(fill_stats(s["sequence"][child]));
          }
          return { "sequence" : l }
        } else if( "fanout" in s ) {
          var f = [];
          for(var child in s["fanout"]) {
            f.push(fill_stats(s["fanout"][child]));
          }
          return { "fanout" : f }          
        } else {
          return {
            "label": s["label"],
            "stats": self.counter(s["stats"]),
            "speed": self.speed(s["stats"])
          }
        }
      }
      return fill_stats(store.getters.diagram(this.id));
    },
    counter :  function() {
      return function(name) {
        if( "counters" in this.model.stats && name in this.model.stats.counters ) {
          return this.model.stats.counters[name];
        }
        return {}
      }
    },
    speed : function() {
      return function(name) {
        if( "timers" in this.model.stats && name in this.model.stats.timers ) {
          var timer = this.model.stats.timers[name];
          return Math.round((timer.total / timer.count) / 1000, 2);
        }
        return null;
      }
    },
    total : function() {
      if( "timers" in this.model.stats && "total" in this.model.stats.timers ) {
        var timer = this.model.stats.timers.total;
        return Math.round(timer.total / timer.count);
      }
      return null;      
    }
  },
  methods: {
    reset: function() {
      $.get(store.getters.env("FA_URL") + "/intake/stats?reset=1")
    },
    play: function() {
      this.playing = true;
      this.poll_stats();
      console.log("starting stats polling loop...");
    },
    stop: function() {
      this.playing = false;
      console.log("stopping stats polling loop...")
    },
    poll_stats : function() {
      if(this.playing) {
        this.fetch_stats();
        // shedule next fetch
        var self = this;
        this.poller = setTimeout(function () { self.poll_stats(); }, this.interval);
      }
    },
    fetch_stats : function() {
      var self = this;
      $.ajax({
        url: store.getters.env("FA_URL") + "/intake/stats",
        type: "GET",
        success: function(response) {
          console.log(response);
          self.model.stats = response;
        },
        error: function(response) {
          app.$notify({
            group: "notifications",
            title: "Could not fetch stats templates...",
            text:  response.responseText,
            type:  "warn",
            duration: 10000
          });
        }
      });
    }
  },
  data: function() {
    return  {
      playing: false,
      poller: null,
      interval: 1000,
      model: {
        stats : {}
      }
    }
  }
});

// set up env store

store.registerModule("ProcessDiagram", {
  state: {
    diagram: {}
  },
  mutations: {
    updated_diagram: function(state, diagram) {
      Vue.set(state.diagram, diagram.id, diagram);
    }
  },
  getters: {
    diagram: function(state) {
      return function(id) {
        return state.diagram[id];
      }
    }
  }
});
