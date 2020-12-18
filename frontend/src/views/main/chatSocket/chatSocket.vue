<template>
  <div id="app">
    <h2>Vue.js WebSocket Tutorial</h2>
    <h3>Send a message</h3>
    <v-form @keyup.enter="sendMessage" @submit.prevent="">
      <v-text-field @keyup.enter="sendMessage" v-model="message"></v-text-field>
      <v-btn v-on:click="sendMessage('hello')">Send Message</v-btn>
    </v-form>
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
@Component
export default class ChatSocket extends Vue {
  message: string = "";
  received: IMessage[] = [];
  connection: WebSocket = new WebSocket("wss://echo.websocket.org");
  created() {
    console.log("Starting connection to WebSocket Server");

    this.connection.onmessage = ((v: ChatSocket) => {
      return function (event) {
        const val = event as IMessage;
        console.log(val);
        v.received.unshift(val);
      };
    })(this);

    this.connection.onopen = function (event) {
      console.log(event);
      console.log("Successfully connected to the echo websocket server...");
    };
  }
  sendMessage() {
    this.connection.send(this.message);
    this.message = "";
  }
}
</script>