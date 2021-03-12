<template>
  <div id="app">
    <h2>Vue.js WebSocket Tutorial</h2>
    <v-btn v-on:click="reset">Reset</v-btn>

    <h3>Send a message</h3>
    <v-form @keyup.enter="sendMessage" @submit.prevent="">
      <v-text-field @keyup.enter="sendMessage" v-model="message"></v-text-field>
      <v-btn v-on:click="sendMessage('hello')">Send Message</v-btn>
    </v-form>
    <div v-for="(errorMessage, index) in chatErrors" v-bind:key="index">
      {{ errorMessage.message }}
    </div>
    <div v-for="(item, index) in received" v-bind:key="index">
      <v-card>
        <v-card-text>
          <template>
            {{ item.data }}
          </template>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
interface IMessage {
  data: string;
  timestamp: number;
}
interface IChatError {
  message: string;
}
@Component
export default class ChatSocket extends Vue {
  public message: string = "";
  public received: IMessage[] = [];
  public chatErrors: IChatError[] = [];
  public connection: WebSocket = new WebSocket("wss://echo.websocket.org");
  public reset() {
    this.received = [];
    this.chatErrors = [];
    // console.log('Starting connection to WebSocket Server');
    new WebSocket("wss://echo.websocket.org");
    this.connection.onmessage = ((v: ChatSocket) => {
      return function (event) {
        try {
          const val = event as IMessage;
          // console.log(val);
          v.received.unshift(val);
        } catch (error) {
          v.chatErrors.push({ message: error.toString() });
        }
      };
    })(this);

    this.connection.onopen = ((cs: ChatSocket) => {
      return (event) => {
        try {
          // console.log(event);
          // console.log('Successfully connected to the echo websocket server...');
        } catch (error) {
          cs.chatErrors.push({ message: error.toString() });
        }
      };
    })(this);
    this.connection.onerror = (err) => {
      this.chatErrors.push({ message: err.toString() });
    };
  }
  public mounted() {
    this.reset();
  }
  public created() {}
  public sendMessage() {
    try {
      this.connection.send(this.message);
      this.message = "";
    } catch (error) {
      this.chatErrors.push({ message: error });
    }
  }
}
</script>
