import React, { Component } from 'react';
import Samples from './components/samples';

class App extends Component {
  state = {
    samples: []
  }
  componentDidMount() {
    fetch('http://127.0.0.1:5000/api/currently-playing/samples')
    .then(res => res.json())
    .then((data) => {
      this.setState({ samples: data })
    })
  }
  render() {
    return (
      <Samples samples={this.state.samples} />
    );
  }
}

export default App;