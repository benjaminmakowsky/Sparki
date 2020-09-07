import React from "react";
import './DataTable.css';

interface Props{
    battery: String
    heading: String
}


export const DatabaseView: React.FC<Props> = ({battery, heading}) => {
    return(
      <table className={"DataTable"}>
        <tr>
          <th className={"LeftTableHeader"}>Battery</th>
          <th className={"CenterTableHeader"}>Heading</th>
          <th className={"RightTableHeader"}>Voltage</th>
        </tr>
        <tr>
          <td className={"TableData"}>{battery}</td>
          <td className={"TableData"}>{heading}</td>
          <td className={"TableData"}>N/A</td>
        </tr>
      </table>
  );
};