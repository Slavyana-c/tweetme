import React, {useEffect, useState} from "react";
import numeral from 'numeral'
import {apiTweetDetail} from "../tweets/lookup";
import {apiProfileDetail, apiProfileFollowToggle} from "./lookup";
import {UserPicture} from "./components";
import {UserDisplay} from "./components";
import {DisplayCount} from "./utils";

function ProfileBadge(props) {
    const {user, didFollowToggle, profileLoading} = props

    let currentVerb = (user && user.is_following) ? 'Unfollow' : 'Follow'
    currentVerb = profileLoading ? 'Loading...' : currentVerb

    const handleFollowToggle = (event) => {
        // console.log(event)
        event.preventDefault()
        if (didFollowToggle && !profileLoading) {
            didFollowToggle(currentVerb)
        }
    }

    return user ? <div>
        <UserPicture user={user} hideLink/>
        <p><UserDisplay user={user} includeFullName hidelink/></p>
        <p><DisplayCount>{user.follower_count}</DisplayCount> {user.follower_count === 1 ? 'Follower' : 'Followers' }</p>
        <p><DisplayCount>{user.following_count}</DisplayCount> Following</p>
        <p>{user.location}</p>
        <p>{user.bio}</p>
        <button className='btn btn-primary' onClick={handleFollowToggle}>{currentVerb}</button>
    </div> : null
}


export function ProfileBadgeComponent(props) {
    const {username} = props
    // lookup
    const [didLookup, setDidLookup] = useState(false);
    const [profile, setProfile] = useState(null)
    const [profileLoading, setProfileLoading] = useState(false)


    const handleBackendLookup = (response, status) => {
        if (status === 200) {
            setProfile(response)
        }
    };

    useEffect(() => {
        if (didLookup === false) {
            apiProfileDetail(username, handleBackendLookup);
            setDidLookup(true)
        }

    }, [username, didLookup, setDidLookup]);

    const handleNewFollow = (actionVerb) => {
        setProfileLoading(true)
        apiProfileFollowToggle(username, actionVerb, (response, status) => {
            if(status === 200) {
                 setProfile(response)
            //                apiProfileDetail(username, handleBackendLookup);
            }
            setProfileLoading(false)
            console.log(response, status)


        })

    }

    return didLookup === false ? 'Loading...' : profile ?
        <ProfileBadge user={profile} didFollowToggle={handleNewFollow} profileLoading={profileLoading}/> : null
}
