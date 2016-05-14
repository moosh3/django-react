import React from "react";

export default (props) => {
  React.render(
    <CommentBox items={props.items}/>,
    document.getElementById('content')
  )
}
