<template>
  <div>
    <header>
        <nav class="navbar navbar-expand-lg navbar-top">
            <div class="container">
            <a class="navbar-brand">
                Texas COVID Drive Thrus
            </a>
            </div>
        </nav>
    </header>
  </div>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
  header {
    height: 10vh;
  }
  .navbar-brand {
    color: white !important;
  }
  .navbar-top {
    background-color: #313a46;
    min-height: 80px;
    color: #98a6ad;
    position: relative;
  }
</style>
