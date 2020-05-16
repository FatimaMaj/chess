'use strict';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {clicks: 0};
  }

  render() {
    return (
      <button onClick={() => this.setState({ clicks: this.state.clicks + 1 }) }>
        Clicks: {this.state.clicks}
      </button>
    );
  }
}

const root = document.querySelector('#root');
ReactDOM.render(<App/>, root);