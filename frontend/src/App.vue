<template>
  <div id="app">
    <header class="header">
      <nav class="nav">
        <router-link to="/" class="nav-link">Главная</router-link>
        <router-link to="/suggest" class="nav-link">Предложить фильм</router-link>
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
  font-family: Arial, sans-serif;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background-color: #2c3e50;
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
  color: white;
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  transition: background-color 0.3s;
  font-size: 0.9rem;
  text-align: center;
  flex: 1;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: #34495e;
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