import {
  Box,
  Button,
  Text,
  Popover,
  PopoverContent,
  PopoverHeader,
  PopoverCloseButton,
  PopoverBody,
  PopoverFooter,
  Portal,
  PopoverTrigger
} from "@chakra-ui/react";
import * as React from "react";
import { Events, ExtraInfoOnPerson, Person } from "../api/api-generated-types";
import { FaInfoCircle } from "react-icons/fa";
import DynamicFAIcon from "./dynamicFAIcon";
import useGetPerson from "../api/useGetPerson";

const ExtraInfoComponent = ({ information, icon, iconColor, url }: ExtraInfoOnPerson) => {
  //@Jorrick ToDo add URL to the equation
  return (
    <Box p={2} style={{ display: "flex", alignItems: "center" }}>
      <DynamicFAIcon icon={icon} color={iconColor} style={{ display: "inline-block" }} />
      <Text style={{ display: "inline-block", marginLeft: "10px" }}>{information}</Text>
    </Box>
  );
};

const LazyLoadingPopoverContent = ({ personUid }: { personUid: number }) => {
  const { data: apiPerson } = useGetPerson({ personUid });

  return (
    <>
      <PopoverHeader mt="5px" pl="20px" pb="10px" style={{fontWeight: "bold", fontSize: "20px"}}>
          {apiPerson ? apiPerson.ldap ?? apiPerson.email : "unknown"}
      </PopoverHeader>
      <PopoverCloseButton pt={"22px"} pr={"22px"} fontSize={"12px"}/>
      <PopoverBody>
        {apiPerson?.imgFilename &&
          <Box mb={"10px"} mt={"10px"}>
            <img
              src={process.env.API_ADDRESS + "person_img/" + apiPerson.imgFilename}
              style={{width: 200, height: 200, borderRadius: 200 / 2, marginLeft: "auto", marginRight: "auto"}}
              alt={"Profile picture"}
            />
          </Box>
        }
        {apiPerson?.extraAttributes.map((extraAttribute: ExtraInfoOnPerson, index) => (
          <ExtraInfoComponent {...extraAttribute} key={index} />
        ))}
      </PopoverBody>
      <PopoverFooter>
        Last updated: {apiPerson?.lastUpdate}
        <br />
        Sync enabled: {apiPerson?.sync ? "True" : "False"}
      </PopoverFooter>
    </>
  );
};

const PersonComponent = ({ person }: { person: Person }) => {
  const initRef = React.useRef();

  return (
    <>
      {person == undefined ? (
        "Unknown error.."
      ) : (
        <Popover placement="left" initialFocusRef={initRef} isLazy lazyBehavior='keepMounted'>
          {({ isOpen, onClose }) => (
            <>
              <PopoverTrigger>
                <Box style={{ cursor: "pointer" }}>
                  <Text mr="10px" style={{ display: "inline-block" }}>{person.ldap ?? person.email}</Text>
                  <Text style={{ display: "inline-block", verticalAlign: "middle", fontSize: "20px" }}>
                    <FaInfoCircle />
                  </Text>
                </Box>
              </PopoverTrigger>
              <Portal>
                <PopoverContent backgroundColor={"#F5F5F5"}>
                    <LazyLoadingPopoverContent personUid={person.uid} />
                </PopoverContent>
              </Portal>
            </>
          )}
        </Popover>
      )}
    </>
  );
};

export default PersonComponent;
