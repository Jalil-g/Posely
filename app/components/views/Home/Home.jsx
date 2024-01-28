import { useState } from 'react';
import { View, Image, StyleSheet } from 'react-native';
import { TouchableOpacity } from 'react-native-gesture-handler';
import { Button, Text } from 'react-native-paper';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

export default function Home({ navigation }) {
    const [gender, setGender] = useState(null);

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'space-evenly' }}>
            <View>
                <Text style={{ alignSelf: "center", fontSize: 50, color: "#663399", fontWeight: "bold", fontFamily: "" }}>POSELY</Text>
                <Text style={{ alignSelf: "center", fontSize: 15, color: "#6C63FF", fontWeight: "bold", fontFamily: "" }}>I would like to pose as a...</Text>
                <View style={{ flexDirection: 'row' }}>
                    <Image source={require('../../../assets/male.png')} style={{ width: 150, height: 150, ...styles.imageShadow }} />
                    <Image source={require('../../../assets/female.png')} style={{ width: 150, height: 150, ...styles.imageShadow }} />
                </View>
            </View>
            <View>
                <Text style={{ alignSelf: "center", fontSize: 30, color: "#6C63FF", fontWeight: "bold", }}>Let's Pose!</Text>
                <Image source={require('../../../assets/pose.png')} style={{ width: 300, height: 200, ...styles.imageShadow }} />
                <TouchableOpacity style={{ alignSelf: "center", backgroundColor: "#663399", padding: 15, borderRadius: 50, margin: 5, ...styles.imageShadow }} onPress={() => navigation.navigate('Camera')} disabled={false}>
                    <MaterialCommunityIcons name="camera-enhance" color={"#fff"} size={50} />
                </TouchableOpacity>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    imageShadow: {
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 5,
        },
        shadowOpacity: 0.36,
        shadowRadius: 6.68,
    }
});