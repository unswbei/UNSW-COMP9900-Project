import React from "react";
import ReactComment from "./ReactComment";

export default function CommentList(props) {
  return (
    <div>
      <h5>
        Comment{props.comments.length > 0 ? "s" : ""}
        <span>({props.comments.length})</span>
      </h5>

      {props.comments.length === 0 ? (
        <div className="text-center">Be the first to comment</div>
      ) : null}

      {props.comments.length > 0 &&
        props.comments.map((comment, index) => (
          <ReactComment
            key={index}
            comment={comment}
            addComment={props.addComment}
            id={props.id}
          />
        ))}
    </div>
  );
}
