import React from 'react';

import 'bulma/css/bulma.css';

const UsersList = (props = {users: []}) => {
  const { users } = props;

  return (
    users.map( user => {
      return (
        <h4 key={user.id} className="box title is-4">
          {user.username}
        </h4>
      );
    })
  );
};

export default UsersList;

