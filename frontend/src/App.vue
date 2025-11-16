<template>
  <div id="app">
    <header class="header">
      <nav class="nav">
        <router-link to="/" class="nav-link">HOME</router-link>
        <router-link to="/suggest" class="nav-link">SUBMISSIONS</router-link>
        <router-link to="/calendar" class="nav-link">CALENDAR</router-link>
      </nav>
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: "Cascadia Code", cascadia;
  min-height: 100vh;
  background-color: #151519;
}

.header {
  background-color: rgb(255, 217, 223);
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  gap: 1rem;
  padding: 0 1rem;
}

.nav-link {
  color: black;
  text-decoration: none;
  padding: 0.75rem 1rem;
  transition: background-color 0.3s;
  font-size: 3rem;
  text-align: center;
  flex: 1;
  text-decoration: solid;
  font-weight: bolder;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: pink;
}

.main {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

/* Мобильные стили */
@media (max-width: 768px) {
  .header {
    padding: 0.75rem 0;
  }
  
  .nav {
    gap: 0.5rem;
    padding: 0 0.75rem;
  }
  
  .nav-link {
    padding: 0.6rem 0.5rem;
    font-size: 0.85rem;
  }
  
  .main {
    padding: 1rem 0.75rem;
  }
}

@media (max-width: 480px) {
  .nav {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .nav-link {
    padding: 0.5rem;
    font-size: 0.8rem;
  }
}
</style>