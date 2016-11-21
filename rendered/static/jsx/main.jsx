import React from 'react';
import ReactDOM from 'react-dom';
import CommentBox from './components/CommentBox.jsx';
import { Button } from 'react-toolbox/lib/button';

export function bootstrap(props) {
  ReactDOM.render(
    <CommentBox comments={props.comments} url={props.url} pollInterval={props.pollInterval} />,
    document.getElementById('content')
  );

  ReactDOM.render(
    <Button label="Hello World!" />,
    document.getElementById('app')
  );
}
