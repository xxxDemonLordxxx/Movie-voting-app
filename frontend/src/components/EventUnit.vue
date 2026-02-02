<template>
    <div class="event-container">
        <div class="buffer"></div>
        <div class="header-block">
            <p>{{eventDate}} {{eventTime}}</p>
            <p>MAIN CAMPUS</p>
        </div>
        <div class="event-block event-text">
            <h3 class="event-title">{{ eventTitle }}</h3>
            <p class="description">{{ eventDescription }}</p>

        </div>
        <div class="event-block more-event">
            <img 
            src='@/assets/more_button.png' 
            @click="$emit('open-event', event)" 
            class="more-button" />
        </div>
        <div class="buffer"></div>
    </div>

</template>

<script>
export default {
  name: 'EventUnit',
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  computed: {
    eventTitle() {
      return this.event?.title || 'No name'
    },
    eventDescription() {
      return this.event?.description || 'No description'
    },
    eventDate() {
        if (!this.event?.date) return ''
        return new Date(this.event.date).toLocaleDateString('ru-RU')
    },
    eventTime() {
        if (!this.event?.date) return ''
        return new Date(this.event?.date).toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit'
        })
    }
  }
}
</script>

<style>

.event-container{
    display: flex;
    flex-direction: row;
    box-sizing:border-box;
    height: 10rem;
    width: 100vw;
    margin-left: -50vw;
    position: relative;
    left: 50%;
    gap: 0.5rem;
}

.header-block{
    background: rgb(78, 32, 82);
    color:black;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: right;
    font-size: 13spx;
    color: white;
    border-color: rgb(199, 107, 208);;
    border-width: 0rem;
    border-style: dotted;
    
}

.event-block{

    display: flex;
    flex-direction: row;
    color: white;
    border-color: rgb(116, 110, 140);
    border-width: 0.1rem;
    border-style: dotted;
    

}

.event-text{
    flex-grow: 5;
    justify-content: space-between;

}

.more-button{
    color: #023730;
    text-align: center;
    font-size: 1rem;
    writing-mode: vertical-rl;
    text-orientation: upright;
    margin: 0.2rem;
    padding: 0;
    background-color: #02373000;
    border: none;
}

h1{
    font-size: 23px;
}

.description{
    overflow-wrap: break-word;
    overflow:hidden;
    padding-left: 0.5rem;
    text-overflow: ellipsis;
    font-size: 0.72rem;
}

.event-title {
    font-family: "Blackout Two AM";
    overflow-wrap: break-word;
    text-overflow: ellipsis;
    overflow:hidden;
}
.more-event{
    width: 1.8rem
}

.buffer{
    border-color: rgb(59, 53, 82);
    border-width: 0.1rem;
    border-style: dotted;
    width: 30rem;
    flex-grow: 5;
}

@media (max-width: 784px) {
.header-block{
    max-width: 20%;
    font-size: 0.75rem
}
.more-event{
    width: 8%
}
}

@media (max-width: 480px) {
 .buffer {
    display: none;
 }
}   

@media (min-width: 785px) {
 .event-text {
    width: 30rem;
 }
}  
</style>