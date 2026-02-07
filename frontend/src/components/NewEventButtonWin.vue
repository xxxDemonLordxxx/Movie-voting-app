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
              <label for="eventDescription" class="input">description:</label>
              <input
                  id="eventDescription"
                  v-model="form.eventDescription"
                  placeholder="write the description of the event"
                  class="input form-input admin-input"
                  required
                  name="eventDescription"
              />
              <label for="eventEnd" class="input">end date:</label>
              <input
                  type="datetime-local"
                  id="eventDate"
                  name="meeting-time"
                  class="input admin-input"
                  v-model="form.eventEnd"
                />
              <button class="btn admin" @click="submitEvent">Submit</button>
          </form>
      </dialog>
    </div>

    <p>
        <button class="btn" @click="confirm">Confirm</button>
        <button class="btn admin" @click="showDialog">New event</button>
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
                eventDescription: '',
                image: '',
            },
            image: {
              object:true
            },
            submitting: false
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
    closeDialog() {
            if (this.dialogRef) {
                this.dialogRef.close();
                this.form.eventTitle = ''; // Clear form on close
            }
        },
    async showConfirmDialog() {
            if (this.dialogRef) {
                this.dialogRef.showModal();
                try {
        const response = await fetch(`http://observational.website/polls/confirm/${parseInt(this.$route.params.id)}`, {
        method: 'PATCH',  // Changed from POST to PATCH
        headers: {
          'Content-Type': 'application/json',
        },
        // Remove the body since poll_id is in the URL
      })
        if (response.ok) {
          alert('Poll status changed')
        } else {
          throw new Error('SENDING ERROR')
        }
      } catch (error) {
        console.error('Error:', error)
        alert('SENDING ERROR')
      } 
    }
    }
    },
    async submitEvent() {
      if (!this.form.eventTitle.trim()) {
        alert('PLEASE, FILL')
        return
      }

      try {
        const response = await fetch('http://observational.website/events/new', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: this.form.eventTitle,
            date: "2026-02-02T14:17:47.745Z",
            description: this.form.eventDescription,
            image: (this.form.image, 'utf-8'),
            event_type_id: "1"
          })
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