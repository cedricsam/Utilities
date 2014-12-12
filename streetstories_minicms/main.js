// hold markers so we can always remove them later
window.currentMarkers = [];
window.currentInfoWindows = [];
window.overheadIsUnconfigured = true;
window.soundOn = true;
window.atInit = true;
window.newSlide = true;

// Script for showing / hiding the opening text
$(function() {
  $("#overlay").click(function(){
    $("#overlay").css("display", "none");
    if (window.atInit) {
        window.atInit = false;
        if (!$("#mappop").is(':visible') && winW > 1020) {
            $("#mappop").slideToggle();
            $("#mappop-over").slideToggle();
            // hacky af but this is a prototype... right?
            setTimeout(function() {
              ensureOverheadConfigured();
            }, 500);
        }
        $("#blurb").fadeIn();
    }
  })
  $("#infoReturn").click(function(){
    if ($(".about").is(':visible')) {
        $(".about").css("display", "none");
    }
    $("#overlay").slideToggle();
  });
  $("#mapToggle").click(function(){
    $("#mappop").slideToggle();
    $("#mappop-over").slideToggle();
    // hacky af but this is a prototype... right?
    setTimeout(function() {
      ensureOverheadConfigured();
    }, 500);
  })
  $("#closeMappop").click(function(){
    $("#mappop").slideToggle();
    $("#mappop-over").slideToggle();
  });
  $(".name").click(function(){
    if ($("#overlay").is(':visible')) {
        $("#overlay").css("display", "none");
    }
    $(".about").slideToggle();
  })
  $("#creditsReturn").click(function(){
    if ($("#overlay").is(':visible')) {
        $("#overlay").css("display", "none");
    }
    $(".about").slideToggle();
  })
  $("#credits-close").click(function(){
    if ($("#overlay").is(':visible')) {
        $("#overlay").css("display", "none");
    }
    $(".about").slideToggle();
  })
  $("#sound-control").click(function(){
    if ($("#sound-control").hasClass("fi-volume")) {
        $("#sound-control").removeClass("fi-volume");
        window.soundOn = false;
        $("#sound-control").addClass("fi-volume-strike");
    } else {
        $("#sound-control").removeClass("fi-volume-strike");
        window.soundOn = true;
        $("#sound-control").addClass("fi-volume");
    }
    $("#sound-control").trigger('soundToggled');
  });
});

function dateIdxIsValid(idx) {
  if (typeof(window.mapInfo) === "undefined" || window.mapInfo === null) {
    console.error("Unable to load map info.");
    return false;
  } else if (idx >= window.mapInfo.length) {
    console.error("No date for index", idx);
    return false;
  }
  return true
}

// called once the map has been created
function initialize() {
  //console.log("running initialize");

  if (dateIdxIsValid(0)) {
    //console.log("add markers for starting location");
    addMarkers(window.mapInfo[0]);
    
    //console.log("configure dates");
    populateDateSelector();
    
    //console.log("kill infowindows if the user changes positions");
    google.maps.event.addListener(window.map, "position_changed", closeInfoWindows);
    google.maps.event.addListener(window.map, "pano_changed", function() {
        if (window.newSlide || window.atInit) {
            window.newSlide = false;
            return 0;
        }
        window.overheadMap.setZoom(16);
        window.overheadMap.setCenter(window.map.getPosition());
    });
    
    //console.log("load a sync'd map into mappop");
    createOverheadMap();
  }
}

function createOverheadMap() {
  window.overheadMap = new google.maps.Map(document.getElementById("mappop"), {
    zoom: 3,
    zoomControl: false,
    scaleControl: true,
    mapTypeControl: false,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  $("#mapToggle").removeClass("loading");
    /*var divclose = document.createElement("div");
    divclose.className = "fi-x";
    divclose.style.zIndex = 10;
    document.getElementById("mappop").appendChild(divclose);*/
}

function ensureOverheadConfigured() {
  if (window.overheadIsUnconfigured === true) {
    window.overheadMap.setStreetView(window.map);
    google.maps.event.trigger(window.overheadMap, "resize");
    //window.overheadMap.setCenter(window.map.getPosition());
    window.overheadMap.setCenter(new google.maps.LatLng(22.353102, 114.187067)); // Lion Rock
    //window.overheadMap.bindTo("center", window.map, "position");
    window.overheadIsUnconfigured = false;
  }
}

function populateDateSelector() {
  $(document).ready(function(){
    //slideIndex=0;
    $('.timeline').slick({
      slidesToShow: 5, //window.mapInfo.length,
      slidesToScroll: 5,
      arrows: true,
      dots: false,
      focusOnSelect: true,
      draggable: true,
      infinite: true,
      speed: 300,
      slidesToShow: 1,
      centerMode: true,
      variableWidth: true,
      onAfterChange: changeDate
    });

    $.each( window.mapInfo, function( index, value ){
      var link_date = 
      '<div><h3 class="text-center slider-tweak">'+value.date+'</h3><p class="text-center slider-headline header-title">'+value.title+'</p></div>';
      $('.timeline').slickAdd(link_date)
    });
 
  });
}

function changeDate() {
  for (var i=0; i<window.mapInfo.length; i++) {
    if (window.mapInfo[i].date == $(".slick-active").children("h3").text()) {
      setDate(i);
    }
  }
}

function addMarkers(info) {
  if (window.map !== null &&
      typeof(info.markers) !== undefined &&
      info.markers !== null &&
      info.markers.length > 0) {
    for (var i=0; i<info.markers.length; i++) {
      addMarker(info.markers[i]);
    }
  }
}

function addMarker(markerInfo) {
  // create marker
  var markerPos = new google.maps.LatLng(markerInfo.lat, markerInfo.lng);
  var markerImg = "";
  if (markerInfo.type === window.markerTypes.family) {
    markerImg = "img/ribbon.png";
  } else if (markerInfo.type === window.markerTypes.gov) {
    markerImg = "img/govdocs.png";
  } else if (markerInfo.type === window.markerTypes.picture) {
    markerImg = "img/picture.png";
  } else if (markerInfo.type === window.markerTypes.video) {
    markerImg = "img/video.png";
  } else if (markerInfo.type === window.markerTypes.news) {
    markerImg = "img/news.png";
  } else if (markerInfo.type === window.markerTypes.social) {
    markerImg = "img/protest.png";
  }
  var marker = new google.maps.Marker({
    position: markerPos,
    map: window.map,
    icon: markerImg,
    title: markerInfo.title
  });

  // create associated infowindow
  var contentString = "<div class='ss-info-window' style='padding: 20px !important;'><div class='ss-info-headline'>"+markerInfo.headline+"</div><div class='ss-info-content "+markerInfo.infotype+"'>";
  if (markerInfo.infotype === window.infoTypes.picture) {
    contentString += "<a href='img/pics/" + markerInfo.content + "' target='_blank'><img src='img/pics/" + markerInfo.content + "' style='width:560px' border='0'/></a>";
  } else if (markerInfo.infotype === window.infoTypes.video) {
    //contentString += '<video width="480" height="270" controls="controls" poster="http://cf.cdn.vid.ly/'+markerInfo.content+'/poster3.jpg"><source src="http://cf.cdn.vid.ly/'+markerInfo.content+'/mp4.mp4" type="video/mp4"><source src="http://cf.cdn.vid.ly/'+markerInfo.content+'/webm.webm" type="video/webm"></video>';
    contentString += '<iframe frameborder="0" allowfullscreen webkitallowfullscreen mozallowfullscreen msallowfullscreen width="560" height="315" name="vidly-frame" src="http://s.vid.ly/embeded.html?link='+markerInfo.content+'&hd=yes&new=1&autoplay=true"><a target="_blank" href="http://vid.ly/'+markerInfo.content+'"><img src="http://vid.ly/'+markerInfo.content+'/poster" /></a></iframe>';
  } else if (markerInfo.infotype === window.infoTypes.youtube) {
    contentString += "<iframe width='560' height='315' src='//www.youtube.com/embed/"+markerInfo.content+"?autoplay=1&amp;rel=0&amp;showinfo=0' frameborder='0' allowfullscreen></iframe>";
  } else if (markerInfo.infotype === window.infoTypes.tweet) {
    contentString += markerInfo.content;
  }
  contentString += "</div>";
  if (markerInfo.credit !== undefined && markerInfo.credit !== null) {
    contentString += "<div class='ss-info-credit'>" + markerInfo.credit + "</div>";
  }
  if (markerInfo.link !== "") {
    contentString += "<div class='ss-info-link'><a href='"+markerInfo.link+"' target='_blank'>Read more...</a></div>";
  }
  contentString += "</div>";

  var markerIW = new google.maps.InfoWindow({
    content: contentString
  });
  google.maps.event.addListener(marker, "click", function() {
    // close open infowindows
    closeInfoWindows();
    // save new infowindow
    window.currentInfoWindows.push(markerIW);
    // show
    markerIW.open(window.map, marker);
    //modifyInfoWindows();
    ga('send', 'event', 'marker', 'open', markerIW.getContent());
  });

  // save marker and infowindow
  window.currentMarkers.push(marker);
}

function closeInfoWindows() {
  while(window.currentInfoWindows.length > 0) {
    window.currentInfoWindows.pop().close();
  }
}

function modifyInfoWindows() {
  var iterator = document.evaluate("//div[contains(@class, 'ss-info-window')]", document, null, XPathResult.UNORDERED_NODE_ITERATOR_TYPE, null );
  try {
    var thisNode = iterator.iterateNext();
    while (thisNode) {
      thisNode = iterator.iterateNext();
    }
  } catch (e) {
    dump( 'Error: Document tree modified during iteration ' + e );
  }
}

// remove old markers, move map to location of (date), add markers
function setDate(dateIdx) {
  if (dateIdxIsValid(dateIdx)) {
    var newInfo = window.mapInfo[dateIdx];
    window.newSlide = true;
    // remove old markers
    while(window.currentMarkers.length > 0) {
      window.currentMarkers.pop().setMap(null);
    }
    // set new location
    var newCenter = new google.maps.LatLng(newInfo.lat, newInfo.lng);
    window.map.setPosition(newCenter);
    if (newInfo.heading) {
      zm = 0;
      pt = 0;
      if (newInfo.pitch !== undefined && newInfo.pitch != "" && !isNaN(+newInfo.pitch)) pt = +newInfo.pitch;
      if (newInfo.zoom !== undefined && newInfo.zoom != "" && !isNaN(+newInfo.zoom)) zm = +newInfo.zoom;
      window.map.setPov({"heading": newInfo.heading, "pitch": pt, "zoom": zm});
    }
    // add new markers
    addMarkers(newInfo);
    if (newInfo.pano !== undefined && newInfo.pano != "") window.map.setPano(newInfo.pano);
    if (newInfo.description !== undefined && newInfo.description != "") {
        var desc = newInfo.description;
        /*if (newInfo.author !== undefined && newInfo.author != "") {
            desc += " <span>― " + newInfo.author + "</span>";
        }*/
        if (true || dateIdx > 0) desc = '<div class="index">View ' + (dateIdx+1) + ' of ' + window.mapInfo.length + '</div> ' + desc;
        $("#blurb").html(desc);
        $("#blurb").fadeIn();
    } else {
        $("#blurb").fadeOut();
    }
    if (dateIdx > 1) {
        if (dateIdx == 9) window.overheadMap.setZoom(12);
        else window.overheadMap.setZoom(13);
        window.overheadMap.setCenter(new google.maps.LatLng(22.2981875,114.170847)); // TST
    } else {
        window.overheadMap.setZoom(10);
        window.overheadMap.setCenter(new google.maps.LatLng(22.353102, 114.187067)); // Lion Rock
    }
    ga('send', 'event', 'slide', 'open', ""+dateIdx);
  }
}

function checkResize () {
    winH = $(window).height();
    winW = $(window).width();
    if (winW <= 1020) {
        $("#mappop").hide();
        $("#mappop-over").hide();
    }
}
var winH = $(window).height();
var winW = $(window).width();
window.addEventListener('resize', checkResize, false);
