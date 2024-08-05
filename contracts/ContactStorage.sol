pragma solidity ^0.8.0;

contract ContactStorage {
    struct Contact {
        string name;
        string email;
        string phone;
    }

    mapping(uint256 => Contact) public contacts;
    uint256 public contactCount;

    event ContactAdded(uint256 id, string name, string email, string phone);

    function addContact(string memory _name, string memory _email, string memory _phone) public {
        contactCount++;
        contacts[contactCount] = Contact(_name, _email, _phone);
        emit ContactAdded(contactCount, _name, _email, _phone);
    }

    function getContact(uint256 _id) public view returns (string memory, string memory, string memory) {
        require(_id > 0 && _id <= contactCount, "Contact does not exist");
        Contact memory contact = contacts[_id];
        return (contact.name, contact.email, contact.phone);
    }
}
