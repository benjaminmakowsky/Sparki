import React from "react";

interface Props {
    text: String;
    second_text?: String;
}

export const TextField: React.FC<Props> = ({text}) => {
    return (
        <div>
            {text}
        </div>
    );
};