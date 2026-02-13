<template>
   <div class="container"> 
      <dialog class="dialog" ref="dialogRef">
          <form @submit.prevent="SubmitEvent" method="dialog">
              <button  
                  type="button" 
                  aria-label="close"
                  @click="closeDialog"
                  formnovalidate
                  class="btn">XXX
              </button>
              <h1 class="title">Create new event</h1>
              <label for="EventTitle" class="input">title:</label>
              <input
                  id="eventTitle"
                  v-model="form.eventTitle"
                  placeholder="write the title of the event"
                  class="input form-input admin-input"
                  required
                  name="eventTitle"
              />
              <label for="eventType" class="input">type:</label>
              <input
                  id="eventType"
                  v-model="form.eventType"
                  placeholder="write the type of the event"
                  class="input form-input admin-input"
                  required
                  name="eventType"
              />
              <label for="poster" class="input">poster:</label>
              <input
                  id="posterImage"
                  v-on:change="form.posterImage"
                  placeholder="add poster"
                  class="input form-input admin-input"
                  type="file"
                  name="poster"
              />
              <label for="eventEnd" class="input">end date:</label>
              <input
                  type="datetime-local"
                  id="eventDate"
                  name="meeting-time"
                  class="input admin-input"
                  v-model="form.eventDate"
                />
              <button class="btn admin" @click="submitEvent">Submit</button>
          </form>
      </dialog>
    </div>

    <p>
        <button class="btn" @click="showDialog">New event</button>
    </p>
</template>

<script>
export default {
    name: 'NewEventButton',
    data() {
        return {
            form: {
                eventTitle: '',
                eventDate: '',
                eventType: '',
                image: '',
            },
            image: {
              object:true
            },
            submitting: false,
        }
    },
    
    mounted() {
        // Get the dialog element reference
        this.dialogRef = this.$refs.dialogRef;
          if (this.dialogRef && this.dialogRef.open) {
        this.dialogRef.close();
      }
      
    },

methods: {
    showDialog() {
            if (this.dialogRef) {
                this.dialogRef.showModal();
            }
        },
    closeDialog() {
            if (this.dialogRef) {
                this.dialogRef.close();
                this.form.eventTitle = ''; // Clear form on close
            }
        },
    async submitEvent() {
        let formData = new FormData();
        const date = new Date(this.form?.eventDate).toISOString();
        if (posterImage.files.length > 0) {
        stri  
        formData.append('image_file', posterImage.files[0]);
        };
        formData.append('title', this.form?.eventTitle);
        formData.append('date', date);
        formData.append('event_type_id', this.form?.eventType);
        

      if (!this.form.eventTitle.trim()) {
        alert('PLEASE, FILL')
        return
      }

      try {
        
        const response = await fetch('http://localhost:8000/events/new', {
          method: 'POST',
          body: formData
        })

        if (response.ok) {
          alert('EVENT CREATED')
          this.resetForm()
          this.closeDialog();
        } else {
          throw new Error('SENDING ERROR')
        }
        
      } catch (error) {
        console.error('Error:', error)
        alert('SENDING ERROR при отправке предложения')
      } finally {
        this.submitting = false
      }
    },
    
    resetForm() {
      this.form = {
        title: '',
        EventStart: '',
        EventEnd:'',
      }
    }
  }
}
</script>

<style>
.admin {
  display: inline-block;
  padding: 6px 12px;
  background-color: rgba(244, 233, 172, 1);
  color: rgb(45, 35, 35);
  text-decoration: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  margin-top: 0.5rem;
  float: right;
}

.admin:hover{
  background-color: rgb(216, 205, 141);
}

.admin-input{
  background-color: rgb(209, 209, 209); 
  margin: 0.2rem;
}

.text{
  margin: 10px;
  font-size: 22px;
}

.dialog {
  display: none
}
.dialog[open] {
  display: block;
  margin: auto;
  width: 63%;
  overflow: hidden;
}

.dialog::backdrop {
    background-color: rgba(0, 0, 0, 0.5); 
}

.input {
  margin: 0.2rem;
  padding: 0.3rem;
}
</style>