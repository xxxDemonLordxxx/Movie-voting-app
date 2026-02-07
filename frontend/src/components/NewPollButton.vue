<template>
   <div class="container"> 
      <dialog class="dialog" ref="dialogRef">
          <form @submit.prevent="SubmitPoll" method="dialog">
              <button  
                  type="button" 
                  aria-label="close"
                  @click="closeDialog"
                  formnovalidate
                  class="btn"
                  >XXX
              </button>
              <h1 class="title">Create new poll</h1>
              <label for="PollTitle" class="input">title:</label>
              <input
                  id="pollTitle"
                  v-model="form.pollTitle"
                  placeholder="write the title of the poll"
                  class="input form-input admin-input"
                  required
                  name="pollTitle"
              />
              <label for="pollDescription" class="input">description:</label>
              <input
                  id="pollDescription"
                  v-model="form.pollDescription"
                  placeholder="write the description of the poll"
                  class="input form-input admin-input"
                  required
                  name="pollDescription"
              />
              <label for="winners" class="input">winners:</label>
              <input
                  id="winners"
                  v-model="form.winners"
                  placeholder="write the number of winners"
                  class="input form-input admin-input"
                  required
                  name="winners"
              />
              <label for="pollEnd" class="input">end date:</label>
              <input
                  type="datetime-local"
                  id="pollEnd"
                  name="meeting-time"
                  class="input admin-input"
                  v-model="form.pollEnd"
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
                pollDescription: '',
                winners: ''
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
        const response = await fetch('http://backend:8000/polls/new', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: this.form.pollTitle,
            start: new Date().toISOString(), // Current date in API format
            end: new Date(this.form.pollEnd).toISOString(),
            description: this.form.pollDescription,
            winners: this.form.winners
          })
        })

        if (response.ok) {
          alert('POLL CREATED')
          this.resetForm()
          this.closeDialog();
          window.location.reload();
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
  border: 3px rgb(45, 35, 35) solid;
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
  margin: 0.5rem;
  padding: 0.3rem;
}
</style>