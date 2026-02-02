<template>
  <div id="app">
    <header class="header">
      <nav class="nav">
        <router-link to="/" class="nav-link">
          <img class="nav-image" src='/public/navigationicons/home.ico'/>HOME</router-link>
        <router-link to="/calendar" class="nav-link">
          <img class="nav-image" src='/public/navigationicons/calendar.ico'/>CALENDAR</router-link>
        <router-link to="/about_us" class="nav-link">
          <img class="nav-image" src='/public/navigationicons/us.ico'/>ABOUT US
            </router-link>          
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
  height:max-content;
  background-color: #151519;
}

.header {
  padding: 25px;
  position: sticky;
  top: 0;
  z-index: 100;
  margin-bottom: 2rem;
}

.nav {
  max-width: 26rem;
  margin: 0 auto;
  display: flex;
  gap: 1rem;
  padding: 0 1rem;
  background: linear-gradient(0deg,rgba(255, 255, 255, 0) 0%, rgba(21, 21, 25, 0.61) 9%, rgba(21, 21, 25, 1) 36%);
}

.nav-link {
  color: black;
  text-decoration: none;
  transition: background-color 0.3s;
  font-size: 1rem;
  text-align: center;
  text-decoration: solid;
  font-weight: bolder;
  display: flex;
  flex-direction: column;
  aspect-ratio: 1 / 1;
  max-height: 100%;
  width: 100%;
  line-height: 1;
  background-color: #ffc2e0;
  clip-path: polygon(100% 50%,93.55% 56.26%,97.97% 64.09%,90.02% 68.28%,92.06% 77.03%,83.25% 78.81%,82.74% 87.79%,73.79% 87.02%,70.77% 95.48%,62.4% 92.22%,57.12% 99.49%,50% 94%,42.88% 99.49%,37.6% 92.22%,29.23% 95.48%,26.21% 87.02%,17.26% 87.79%,16.75% 78.81%,7.94% 77.03%,9.98% 68.28%,2.03% 64.09%,6.45% 56.26%,0% 50%,6.45% 43.74%,2.03% 35.91%,9.98% 31.72%,7.94% 22.97%,16.75% 21.19%,17.26% 12.21%,26.21% 12.98%,29.23% 4.52%,37.6% 7.78%,42.88% 0.51%,50% 6%,57.12% 0.51%,62.4% 7.78%,70.77% 4.52%,73.79% 12.98%,82.74% 12.21%,83.25% 21.19%,92.06% 22.97%,90.02% 31.72%,97.97% 35.91%,93.55% 43.74%);
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: hsl(338, 100%, 82%);
}

.main {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

.nav-image {
  vertical-align: middle;
  display: inline-block;
  align-self: center;
  height: 60%;
  padding-top: 15%;
  filter: drop-shadow(0.7rem 0.7rem 0.7rem  rgb(227, 113, 227));
}


/* Мобильные стили */
@media (max-width: 768px) {
  .header {
    padding: 0;
    padding-left: 0rem;
    padding-right: 0rem;
  }
  
  .nav {
    gap: 0.3rem;
    padding: 0 0.75rem;
  }
  
  .nav-link {
    font-size: 0.85rem;
    
  }
  
  .main {
    padding: 1rem 0.75rem;
  }
}

@media (max-width: 480px) {
  .nav {
    max-width: 80vw;
    gap: 0.25rem;
  }

}

@media (min-width: 768px) {
  .header{
    margin-left: 3rem;
    margin-right: 3rem;
  }
}
</style>