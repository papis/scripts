<template>
  <md-list-item>
    <div v-for="i in Object.keys(item)" :key="i.id">
      <md-icon>{{i}}</md-icon>
      <span class="md-list-item-next">
        {{i}} {{item[i]}}
      </span>
    </div>
  </md-list-item>
</template>

<script>
export default {
  name: 'Item',
  props: {
    item: {}
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.md-list {
  width: 320px;
  max-width: 100%;
  display: inline-block;
  vertical-align: top;
  border: 1px solid rgba(#000, .12);
}
</style>
