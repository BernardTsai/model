versionA = new Slider( "#versionA" )
versionB = new Slider( "#versionB" )

versionA.on( 'change', setVersionA )


  // fill the list of contexts
  function listContexts( contexts )
  {
    $("#contexts").find('a').remove();

    entries = contexts.split(/\r?\n/);

    for (var i in entries)
    {
      entry = entries[i];
      if (entry != "")
      {
        html = "<a class=\"dropdown-item\" href=\"javascript:selectContext(\'" + entry + "\')\">" + entry + "</a>"

        $('#contexts').append( html );
      }
    }

    versionA.setValue(1)
    versionA.setAttribute( "max", 1)

    versionB.setValue(1)
    versionB.setAttribute( "max", 1)

    $("#modelA").val( "" );
    $("#modelB").val( "" );
  }

  // change context
  function selectContext( context )
  {
    $("#context>a").text( context )

    $.ajax( {type: "get", url: "/context/" + context,   success: listVersions });

    $("#model").val( "" );
  }

  // fill the list of versions
  function listVersions( versions )
  {
    max     = 1
    entries = versions.split(/\r?\n/);

    for (var i in entries)
    {
      entry = entries[i];
      if (entry != "")
      {
        max = Math.max( parseInt(entry), max )
      }
    }

    versionA.setAttribute( "max", max )
    versionA.setValue(max)
    versionB.setAttribute( "max", max )
    versionB.setValue(max)

    $("#modelA").val( "" );

    context = $("#context>a").text()
    $.ajax( {type: "get", url: "/context/" + context + "/" + max, success: setModel });
  }

  // change version
  function selectVersion( version )
  {
    $("#version>a").text( version )

    context = $("#context>a").text()

    $.ajax( {type: "get", url: "/context/" + context + "/" + version,   success: setModel });

    $("#model").val( "" );
  }

  // change version
  function setVersionA()
  {
    context = $("#context>a").text()
    version = versionA.getValue()

    $("#modelA").val( "" );

    $.ajax( {type: "get", url: "/context/" + context + "/" + version,   success: setModel });
  }

  // routine to set the model
  function setModel( model )
  {
    $("#modelA").val( model );
  }

  // handlers

  // load initial content
  $.ajax( {type: "get", url: "/context",   success: listContexts });
