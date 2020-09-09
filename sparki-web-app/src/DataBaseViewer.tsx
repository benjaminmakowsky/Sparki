import React from "react";
import './DataTable.css';

interface Props {
    battery: String
    heading: String
    light: String
}


export const DatabaseView: React.FC<Props> = ({battery, heading, light}) => {
    return (
        <table cellSpacing={0} className={"DataTable"}>
            <thead>
                <tr>
                    <th colSpan={1} className={"RobotTitle"}>Sparki</th>
                    <th colSpan={2} className={"HardwareInfo"}>
                        <div>SKU: 12345678</div>
                        <div>MAC: ff:ff:ff:c3:4d:df</div>
                        <div>UPTIME: 5h 6m</div>
                    </th>
                </tr>
            </thead>
            <tbody className={"DataTableBody"}>
                <tr>
                    <th className={"LeftTableHeader"}>Battery</th>
                    <th className={"CenterTableHeader"}>Heading</th>
                    <th className={"RightTableHeader"}>Ambient Light</th>
                </tr>
                <tr className={"TableData"}>
                    <td className={"TableDataBottomLeft"}>{battery}</td>
                    <td>{heading}</td>
                    <td className={"TableDataBottomRight"}>{light}</td>
                </tr>
            </tbody>
        </table>
    );
};