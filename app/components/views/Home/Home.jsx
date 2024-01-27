import { useState } from 'react';
import { View, Image, StyleSheet } from 'react-native';
import { Button, Text } from 'react-native-paper';

export default function Home({ navigation }) {
    const [gender, setGender] = useState(null);

    return (
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'space-around' }}>
            <View>
                <Text style={{ alignSelf: "center", fontSize: 15, color: "#6C63FF", fontWeight: "bold", fontFamily: "" }}>I would like to pose as a...</Text>
                <View style={{ flexDirection: 'row' }}>
                    <Image source={require('../../../assets/male.png')} style={{ width: 150, height: 150, ...styles.imageShadow }} />
                    <Image source={require('../../../assets/female.png')} style={{ width: 150, height: 150, ...styles.imageShadow }} />
                </View>
            </View>
            <Button icon="camera" mode="contained" onPress={() => navigation.navigate('Camera')} disabled={false}>Click picture</Button>
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