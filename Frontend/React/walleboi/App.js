import React, { isValidElement, Component } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  AsyncStorage
} from 'react-native';
import init from './node_modules/react_native_mqtt'
init({
  size: 10000,
  storageBackend: AsyncStorage,
  defaultExpires: 1000 * 3600 * 24,
  enableCache: true,
  reconnect: true,
  sync: {

  }
})
function onConnect() {
  console.log("ye")
  client.subscribe("abbexpectmore@gmail.com/light")
}
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}
function onMessageArrived(message) {
  console.log("onMessageArrived:" + message.payloadString);
}
const client = new Paho.MQTT.Client("maqiatto.com", 8883, 'clientID');
// Set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

client.connect({
  userName: "abbexpectmore@gmail.com",
  password: "hej",
  onSuccess: onConnect,
})


export default class reactApp extends Component {
  constructor() {
    super()
    this.state = {
      myText: 'My Original Text'
    }
  }
  updateText = () => {
    this.setState({ myText: 'My changed text!' })
  }
  sendMessage = () => {
    var mess = `(0:0:90)`
    var message = new Paho.MQTT.Message(mess);
    message.destinationName = "abbexpectmore@gmail.com/ctrl";
    client.send(message);
    console.log(this.map(10, 0, 20, 0, 100))
  }
  map = (value, x1, y1, x2, y2) => (value - x1) * (y2 - x2) / (y1 - x1) + x2;
  render() {
    return (
      <View style={styles.container}>
        <Text onPress={this.updateText}>
          {this.state.myText}
        </Text>
        <TouchableOpacity
          onPress={this.sendMessage}
        >
          <Text style={{ fontSize: 30 }}>MQTT</Text>
        </TouchableOpacity>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
  }
});
