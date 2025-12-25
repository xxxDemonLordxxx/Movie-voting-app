<template>
   <div class="container"> 
      <dialog class="dialog" ref="dialogRef">
          <form @submit.prevent="SubmitPoll" method="dialog">
              <button  
                  type="button" 
                  aria-label="close"
                  @click="closeDialog"
                  formnovalidate>XXX
              </button>
              <h1 class="title admin" id="CreatePollid">Create new poll</h1>
              <label for="PollTitle" class="input">title:</label>
              <input
                  id="pollTitle"
                  v-model="form.pollTitle"
                  placeholder="write the title of the poll"
                  class="input form-input"
                  required
                  name="pollTitle"
              />
              <label for="pollEnd" class="input">end date (1 week preset):</label>
              <input
                  type="datetime-local"
                  id="pollEnd"
                  name="meeting-time"
                  value="2018-06-12T19:30"
                  class="input"
                />
              <button class="btn admin" @click="submitPoll">Submit</button>
          </form>
      </dialog>
    </div>

    <p>
        <button class="btn" @click="showDialog">New poll</button>
    </p>
</template>

<script>
export default {
    name: 'NewPollButton',
    data() {
        return {
            form: {
                pollTitle: '',
                pollStart: '',
                pollEnd: '',
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
    showDialog() {
            if (this.dialogRef) {
                this.dialogRef.showModal();
            }
        },
    closeDialog() {
            if (this.dialogRef) {
                this.dialogRef.close();
                this.form.pollTitle = ''; // Clear form on close
            }
        },
   
    async submitPoll() {
      if (!this.form.pollTitle.trim()) {
        alert('PLEASE, FILL')
        return
      }

      try {
        const response = await fetch('http://localhost:8000/polls/new', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: this.form.pollTitle,
            start: new Date().toISOString(), // Current date in API format
            end: "2025-12-24T21:22:43.383Z",
          })
        })

        if (response.ok) {
          alert('POLL CREATED')
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
        PollStart: '',
        PollEnd:'',
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
  margin: 0.5rem;
}

.admin:hover{
  background-color: rgb(216, 205, 141);
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
  width: 80%;
}

.dialog::backdrop {
    background-color: rgba(0, 0, 0, 0.5); 
}

.input {
  margin: 0.5rem;
}
</style>