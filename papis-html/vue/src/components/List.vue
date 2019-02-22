<template>
  <div>
    <md-field>
      <label>Search</label>
      <md-input v-model="search"></md-input>
    </md-field>
    <md-list>
      <Item v-for="item in items_to_show" :key="item.id" :item="item"/>
    </md-list>
  </div>
</template>

<script>
import Item from './Item.vue'
import $ from 'jquery'

export default {
  name: 'List',
  components: {
    Item
  },
  computed: {
    items_to_show: function() {
      var result = [];
      this.getItems();
      var re = new RegExp(this.search);
      this.items.forEach(function (el) {
        if (el.__match_string.match(re)) {
          result.push(el);
        }
      });
      return result;
    },
  },
  data() {
    //var retrieved_json = [
    //  {id: 0, name: "blah", year: "blih"},
    //  {id: 1, name: "ier", year: "1999"},
    //  {id: 1, name: "ier", year: "1999"},
    //];
    return {
      items: [],
    }
  },
  methods: {
    getItems: function() {
      var self = this;
      $.getJSON('./lib.json', function(data) {
        self.items = data;
        self.items.forEach(function (el, index){
          el.__match_string = Object.values(el).join("");
          el.__id = index;
        });
      });
    },
  },
  mounted() {
    this.getItems()
  },
  props: {
    search: String,
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>

