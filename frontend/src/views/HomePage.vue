<template>
  <div class="home">
    <h1>CURATORIAL OFC VOTING</h1>
    <p>Thats how we doing it round here. All because we are so fun and democratic.</p>
    <div class="actions">
      <router-link to="/polls" class="btn btn-primary">TO THE POLLS</router-link>
    </div>
    
  
  </div>
</template>



<style scoped>
.home {
  text-align: center;
}

.actions {
  margin: 2rem 0;
}

.btn {
  display: inline-block;
  padding: 12px 24px;
  background-color: #065f53;
  color: white;
  text-decoration: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  margin: 0.5rem;
}

.btn-primary {
  background-color: #065f53;
}

.btn-primary:hover {
  background-color: #0f7f70;
}

.btn-secondary {
  background-color: #95a5a6;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.suggestions-section {
  margin-top: 2rem;
  text-align: left;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.loading, .empty, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

h1 {
  color: white;
  text-align: center;

}

p {
  color: rgba(244, 233, 172, 1);
}
/* Мобильные стили */
@media (max-width: 768px) {
  .home h1 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  
  .suggestions-section h2 {
    font-size: 1.3rem;
  }
  
  .btn {
    padding: 10px 20px;
    font-size: 14px;
    margin: 0.25rem;
  }
  
  .actions {
    margin: 1.5rem 0;
  }
  
  .suggestions-section {
    margin-top: 1.5rem;
  }
}

@media (max-width: 480px) {
  .home h1 {
    font-size: 1.3rem;
  }
  
  .suggestions-section h2 {
    font-size: 1.2rem;
  }
  
  .btn {
    padding: 8px 16px;
    font-size: 13px;
    width: 100%;
    margin: 0.25rem 0;
  }
  
  .actions {
    margin: 1rem 0;
  }
  
  .loading, .empty, .error {
    padding: 1.5rem;
    font-size: 0.9rem;
  }
}
</style>