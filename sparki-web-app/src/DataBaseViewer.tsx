import React from "react";
import './DataTable.css';

interface Props{
    battery: String
    heading: String
    light: String
}


export const DatabaseView: React.FC<Props> = ({battery, heading, light}) => {
    return(
      <table className={"DataTable"}>
        <tr>
          <th className={"LeftTableHeader"}>Battery</th>
          <th className={"CenterTableHeader"}>Heading</th>
          <th className={"RightTableHeader"}>Ambient Light</th>
        </tr>
        <tr>
          <td className={"TableData"}>{battery}</td>
          <td className={"TableData"}>{heading}</td>
          <td className={"TableData"}>{light}</td>
        </tr>
      </table>
  );
};