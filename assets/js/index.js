import React from "react";
import App from "./components/App";

export default (props) => {
  React.render(
    <NavVar items={props.items}/>,
    document.getElementById('content')
  )
}
