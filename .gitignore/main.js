const Discord = require('discord.js');
const myBot = new Discord.Client();
const prefix = '-';
var emojiyes = 'β';
var emojino = 'β';
var emojidelete = 'ποΈ';
var emojiquestion = 'β';
var name = '';
var channell;
var titlee;
var nomm;
var messagee;
var acceptedd;
var imageurll
var maybee
var hourr;
var nameauthorr;
var acceptedList = [];
var maybeList = []
var messverif;
var msgtodelete;


function hook(channel, title, nom , message, hour, nameauthor, accepted, maybe, imageurl) {
    channell = channel;
    titlee = title;
    nomm = nom;
    messagee = message;
    hourr = hour;
    nameauthorr = nameauthor;
    acceptedd = accepted;
    maybee = maybe;
    imageurll = imageurl;

    var msg = new Discord.MessageEmbed();
        msg.setTitle(title)
        msg.setThumbnail(imageurl)  
        msg.setFooter('Demande faite par ' + nameauthorr);
        msg.addField(emojiyes + "**Inscrits :** \n", accepted + '\n ββββββ', true)
        msg.addField(emojiquestion + "**Peut-Γͺtre :** \n", maybe + '\n ββββββ', true)
        msg.setDescription(nom + '\n'
        + '\n'
        + messagee + '\n' 
        + 'ββββββ\n' 
        + '**DΓ©collage : ** \n' + hour + '\n' 
        + 'ββββββ\n');
        msg.addField("**RΓ©agit avec :**", 'β' + ' Si tu viens - ' + emojiquestion  + "Si tu n'es pas sur d'Γͺtre la -\n" + "ποΈ Pour supprimer ta demande")
    return msg;
}

myBot.login(process.env.TOKEN);

function ListToString(List) {
    var str = '';
    for(let i = 0; i < List.length; i ++) {
        if(List[i].startsWith("> ")) {
            List[i] = List[i].slice(2, List[i].length)
        }
        if(i === List.length - 1) {
            str = str + '> ' + List[i]
        }
        else {
            str = str + '> ' + List[i] + '\n'
        }
    }
    return str;
}

function IsStringTheSame(str1, str2) {
    var i = 0;
    var j = 0;
    var common = "";
    var begin = false;
    var stop = false;
    var strmin = "";
    var strmax = "";
    if(str1 > str2) {
        strmin = str2;
        strmax = str1;
    }
    else {
        strmin = str1;
        strmax = str2;
    }
    while(i < strmin.length && j < strmax.length && stop === false) {
        if(strmin[i] === strmax[j]) {
            begin = true;
            common = common + strmin[i]
            i += 1;
            j += 1;
        }
        else {
            j += 1;
            if(begin === true) {
                stop = true;
            }
        }
    }
    return common;
}

async function AddModifyDemande(bot, channelID, messageID, username, accormay) {
    myBot.guilds.cache.get(channelID).channels.cache.forEach(ch => {
        if (ch.type === 'text'){
            ch.messages.fetch({
                limit: 100  
            }).then(messages => {
                const msgs = messages.filter(m => m.author.id === bot.id)
                msgs.forEach(m => {
                    if(m.id === messageID) {
                        if(accormay === true) {
                            acceptedList = []
                            if(acceptedd != "") {
                                acceptedList = acceptedd.slice().split('\n')
                            }
                            acceptedList.push(username)
                            acceptedd = "";

                            var dak = ListToString(acceptedList)
                            var newmsg = hook(channell, titlee, nomm, messagee, hourr, nameauthorr, dak , maybee, imageurll)
                        }
                        else {
                            maybeList = []
                            if(maybee != "") {
                                maybeList = maybee.slice().split('\n')
                            }
                            maybeList.push(username)
                            maybee = "";
                            var peutetre = ListToString(maybeList)
                            var newmsg = hook(channell, titlee, nomm, messagee, hourr, nameauthorr, acceptedd, peutetre, imageurll)
                        }
                        m.edit(newmsg);
                    }
                })
            })
        } else {
            return;
        }
    })
}

async function RemoveModifyDemande(bot, channelID, messageID, username, accormay) {
    myBot.guilds.cache.get(channelID).channels.cache.forEach(ch => {
        if (ch.type === 'text'){
            ch.messages.fetch({
                limit: 100  
            }).then(messages => {
                const msgs = messages.filter(m => m.author.id === bot.id)
                msgs.forEach(m => {
                    if(m.id === messageID) {
                        if(accormay === true) {
                            let acceptedList = acceptedd.slice().split("\n");
                            for(let l = 0; l < acceptedList.length; l ++) {
                                var complistname = IsStringTheSame(acceptedList[l], username)
                                if(complistname === username) {
                                    acceptedList.splice(l, 1)
                                }
                            }
                            acceptedd = "";
                            acceptedd = ListToString(acceptedList);
                            var newmsg = hook(channell, titlee, nomm, messagee, hourr, nameauthorr, acceptedd, maybee, imageurll)
                        }
                        else {
                            let maybeList = maybee.slice().split("\n");
                            for(let k = 0; k < maybeList.length; k ++) {
                                var complistname = IsStringTheSame(maybeList[k], username)
                                if(complistname === username) {
                                    maybeList.splice(k, 1)
                                }
                            }
                            maybee = "";
                            maybee = ListToString(maybeList);
                            var newmsg = hook(channell, titlee, nomm, messagee, hourr, nameauthorr, acceptedd, maybee, imageurll)
                        }
                        m.edit(newmsg);
                    }
                })
            })
        } else {
            return;
        }
    })
}

myBot.on('messageReactionAdd',(reaction, user) =>{
    if(reaction.emoji.name === emojiyes && user.username != myBot.user.username){
        let message = reaction.message;
        name = user.username;
        AddModifyDemande(myBot.user, '700648629693710356', message.id,'<@' + user.id + '>', true)

    }
    if(reaction.emoji.name === emojiquestion && user.username != myBot.user.username) {
        let message = reaction.message
        name = user.username;
        AddModifyDemande(myBot.user, '700648629693710356', message.id, '<@' + user.id + '>', false)
    }
    if(reaction.emoji.name === emojidelete && user.username != myBot.user.username && user.username === nameauthorr && !reaction.message.content.startsWith('Es')) {
        let message = reaction.message
        msgtodelete = message
        var chan = message.channel;
        messverif = "Es-tu sur de vouloir annuler ta demande ?"
        chan.send(messverif)
    }
    if(reaction.emoji.name === emojiyes && user.username != myBot.user.username && user.username === nameauthorr && reaction.message.content.startsWith('Es')) {
        let  message = reaction.message
        msgtodelete.delete();
        message.delete();
        message.channel.send("La demande d'activitΓ© de " + nameauthorr +" a Γ©tΓ© annulΓ©e.")
    }
    if (reaction.emoji.name === emojino && user.username != myBot.user.username && user.username === nameauthorr && reaction.message.content.startsWith('Es')) {
        let message = reaction.message
        message.delete();
        msgtodelete.reactions.cache.get(emojidelete).remove()
        msgtodelete.react(emojidelete);
    }

})

myBot.on('messageReactionRemove',(reaction, user) =>{
    if(reaction.emoji.name === emojiyes && user.username != myBot.user.username){
        let message = reaction.message;
        name = user.username;
        RemoveModifyDemande(myBot.user, '700648629693710356', message.id, '<@' + user.id + '>' , true)
    }
    if(reaction.emoji.name === emojiquestion && user.username != myBot.user.username) {
        let message = reaction.message
        name = user.username;
        RemoveModifyDemande(myBot.user, '700648629693710356', message.id, '<@' + user.id + '>', false)
    }   
})

myBot.on('message', data => {
    if(data.author.id == myBot.user.id && !data.content.startsWith('La') && !data.content.startsWith('Es') && !data.content.startsWith("<")) {
        console.log("juste avant")
        data.react(emojiyes);
        data.react(emojiquestion);
        data.react(emojino);
        data.react(emojidelete);
    }
    if(data.author.id == myBot.user.id && data.content.startsWith('Es')) {
        data.react(emojiyes)
        data.react(emojino)
    }
    //accepted.push(data.author.username)
    if (data.content.startsWith(prefix + 'demande')){
        data.delete();
        if(data.content === prefix + 'demande') {
            return hook(message.channel, 'Voila comment Γ§a marche :', '-demande(raid/pve/pvp/gambit) ActivitΓ© <titre>, <message>\n')
        }

        else if(data.content.startsWith(prefix + 'demanderaid')) {
            data.reply('<@&738428529506517002>')
            .then(msg => {
                msg.delete()
            })
            let hookArgs = data.content.slice(prefix.length + 11).split(";");
            var mess = hook(data.channel, "[(π Demande de Raid π)]", hookArgs[0] , hookArgs[1], hookArgs[2], data.author.username, "", "", 'https://cdn.discordapp.com/emojis/626928125967597568.png');
            data.channel.send(mess)
        }

        else if(data.content.startsWith(prefix + 'demandepve')) {
            data.reply('<@&625416369260855330')
            .then(msg => {
                msg.delete()
            })
            let hookArgs = data.content.slice(prefix.length + 10).split(";");
            var mess = hook(data.channel,"[(π Demande PVE π)]", hookArgs[0], hookArgs[1], hookArgs[2], data.author.username, "", "", 'https://cdn.discordapp.com/emojis/626928103175749632.png');
            data.channel.send(mess)
        }

        else if(data.content.startsWith(prefix + 'demandepvp')) {
            data.reply('<@&618699227949957133>')
            .then(msg => {
                msg.delete()
            })
            let hookArgs = data.content.slice(prefix.length + 10).split(";");
            hook(data.channel, "[(π Demande PVP π)]", hookArgs[0], hookArgs[1], hookArgs[2], data.author.username, "", "", "https://cdn.discordapp.com/emojis/626928115473711104.png");
        }

        else if(data.content.startsWith(prefix + 'demandegambit')) {
            data.reply('<@&625415777146634240>')
            .then(msg => {
                msg.delete()
            })
            let hookArgs = data.content.slice(prefix.length + 13).split(";");
            hook(data.channel, "[(π Demande Gambit π)]", hookArgs[0], hookArgs[1], hookArgs[2], data.author.username, "", "", "https://cdn.discordapp.com/emojis/626928076059574273.png");            
        }

        else if(data.content.startsWith(prefix + 'demandetriomphe')) {
            //data.reply('<@&700398600303411242>')
            //.then(msg => {
            //    msg.delete()
            //})
            let hookArgs = data.content.slice(prefix.length + 10).split(";");
            hook(data.channel, "[(π Demande d'activitΓ© π)]", hookArgs[0], hookArgs[1], hookArgs[2]);
        }

        else{
            let hookArgs = data.content.slice(prefix.length + 8).split(";");
            var mess = hook(data.channel,"[(π Demande d'activitΓ© π)]",'__**' + hookArgs[0] + '**__', hookArgs[1], hookArgs[2], data.author.username, "", "", "https://cdn.discordapp.com/attachments/626264273651236894/627285109174829056/Fichier_2.png")
            data.channel.send(mess);
    }}});
